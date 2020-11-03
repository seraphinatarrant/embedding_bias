# This code is improved so as to report new and more relevant metrics

import os
import sys
import torch
import torch.autograd as autograd
import torch.nn.functional as F


#### NEW ####
# Packages for reporting f1, precision and recall
from sklearn.metrics import f1_score, precision_score, recall_score
#### NEW ####


def train(train_iter, dev_iter, model, args):
    if args.cuda:
        model.cuda()

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    steps = 0
    best_acc = 0
    last_step = 0
    model.train()
    for epoch in range(1, args.epochs+1):
        for batch in train_iter:
            feature, target = batch.text, batch.label
            feature = feature.data.t()
            target = target.data.sub(1)  # batch first, index align
            if args.cuda:
                feature, target = feature.cuda(), target.cuda()

            optimizer.zero_grad()
            logit = model(feature)
            loss = F.cross_entropy(logit, target)
            loss.backward()
            optimizer.step()

            steps += 1
            if steps % args.log_interval == 0:
                corrects = (torch.max(logit, 1)[1].view(target.size()).data == target.data).sum()
                accuracy = 100.0 * corrects/batch.batch_size
                if not args.no_display:
                     sys.stdout.write(
                         '\rBatch[{}] - loss: {:.6f}  acc: {:.4f}%({}/{})'.format(steps, 
                                                                                  loss.item(), 
                                                                                  accuracy.item(),
                                                                                  corrects.item(),
                                                                                  batch.batch_size))
            if steps % args.test_interval == 0:
                dev_acc = eval(dev_iter, model, args)
                if dev_acc > best_acc:
                    best_acc = dev_acc
                    last_step = steps
                    if args.save_best:
                        save(model, args.save_dir, 'best', steps)
                        #### NEW ####
                        save(model, "./cnn/snapshot/", "best", "model")
                        #### NEW ####
                else:
                    if (steps - last_step >= args.early_stop) and not args.no_display:
                        print('early stop by {} steps.'.format(args.early_stop))
            elif steps % args.save_interval == 0:
                save(model, args.save_dir, './cnn/snapshot', steps)


def eval(data_iter, model, args):
    model.eval()
    corrects, avg_loss = 0, 0
    for batch in data_iter:
        feature, target = batch.text, batch.label
        feature.t_(), target.sub_(1)  # batch first, index align
        if args.cuda:
            feature, target = feature.cuda(), target.cuda()

        logit = model(feature)
        loss = F.cross_entropy(logit, target, size_average=False)

        avg_loss += loss.item()
        corrects += (torch.max(logit, 1)
                     [1].view(target.size()).data == target.data).sum()
        
        
        #### NEW ####
        # Reports the relevant metrics when testing
        if args.test:
            output = logit.clone()
            _, predicted = torch.max(output, 1)
            predicted = predicted.cpu()
            target = target.cpu()
            precision = precision_score(y_true=target, y_pred=predicted, average='weighted')
            recall = recall_score(y_true=target, y_pred=predicted, average='weighted')
            f1 = f1_score(y_true=target, y_pred=predicted, average='weighted')
        #### NEW ####
            

    size = len(data_iter.dataset)
    avg_loss /= size
    accuracy = 100.0 * corrects/size
    if not args.no_display:
         print('\nEvaluation - loss: {:.6f}  acc: {:.4f}%({}/{}) \n'.format(avg_loss, 
                                                                            accuracy, 
                                                                            corrects, 
                                                                            size))
    
    #### NEW ####
    # Saves the relevant metrics if a results path is selected
    if args.results_path is not None:
        save_test(args, precision, recall, f1, accuracy)
    #### NEW ####
    
    return accuracy


#### NEW ####
def save_test(args, precision, recall, f1, accuracy):
    string = "Precision: {:.3f}\nRecall: {:.3f}\nF1-Score: {:.3f}\n".format(precision,recall,f1)
    with open(args.results_path,'w', encoding="utf8") as ff:
        ff.write(string)
        ff.write("Accuracy: {:.3f}\n".format(accuracy))
#### NEW ####
        

def predict(text, model, text_field, label_feild, cuda_flag):
    assert isinstance(text, str)
    model.eval()
    text = text_field.preprocess(text)
    text = [[text_field.vocab.stoi[x] for x in text]]
    x = torch.tensor(text)
    x = autograd.Variable(x)
    if cuda_flag:
        x = x.cuda()
    print(x)
    output = model(x)
    _, predicted = torch.max(output, 1)
    return label_feild.vocab.itos[predicted.item()+1]


def save(model, save_dir, save_prefix, steps):
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    save_prefix = os.path.join(save_dir, save_prefix)
    save_path = '{}_steps_{}.pt'.format(save_prefix, steps)
    torch.save(model.state_dict(), save_path)
