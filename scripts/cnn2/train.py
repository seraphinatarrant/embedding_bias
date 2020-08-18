import os
import sys
import torch
import torch.autograd as autograd
import torch.nn.functional as F
import torch.nn as nn


### NEW
from sklearn.metrics import f1_score, precision_score, recall_score
import numpy as np


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
            feature, target = batch.text, getattr(batch, args.label)
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
                        #save(model, args.save_dir, 'best', steps)
                        #print(args.save_dir,"\n",steps)
                        save(model, "./cnn2/snapshot/", "best", "model"+args.label)
                else:
                    if steps - last_step >= args.early_stop:
                        print('early stop by {} steps.'.format(args.early_stop))
            #elif steps % args.save_interval == 0:
            #    save(model, args.save_dir, './cnn/snapshot', steps)


def eval(data_iter, model, args):
    model.eval()
    corrects, avg_loss = 0, 0
    for batch in data_iter:
        feature, target = batch.text, getattr(batch, args.label)
        feature.t_(), target.sub_(1)  # batch first, index align
        if args.cuda:
            feature, target = feature.cuda(), target.cuda()

        logit = model(feature)
        loss = F.cross_entropy(logit, target, size_average=False)

        avg_loss += loss.item()
        corrects += (torch.max(logit, 1)
                     [1].view(target.size()).data == target.data).sum()
        
        
        ### NEW
        if args.test:
            output = logit.clone()#.cpu()
            _, predicted = torch.max(output, 1)
            predicted = predicted.cpu()
            target = target.cpu()
            #predicted = predicted.numpy()
            #_, trues = torch.max(target, 1)
            #print(logit.shape)
            #print(target)
            #print(predicted)
            precision = precision_score(y_true=target, y_pred=predicted, average='weighted')
            recall = recall_score(y_true=target, y_pred=predicted, average='weighted')
            f1 = f1_score(y_true=target, y_pred=predicted, average='weighted')
            

    size = len(data_iter.dataset)
    avg_loss /= size
    accuracy = 100.0 * corrects/size
    print('\nEvaluation - loss: {:.6f}  acc: {:.4f}%({}/{}) \n'.format(avg_loss, 
                                                                       accuracy, 
                                                                       corrects, 
                                                                       size))
    if args.results_path is not None:
        save_test(args, precision, recall, f1, accuracy)
    
    return accuracy



"""
def train(train_iter, dev_iter, model, args):
    if args.cuda:
        model.cuda()
    print(torch.cuda)

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    steps = 0
    best_acc = 0
    last_step = 0
    model.train()
    
    for epoch in range(1, args.epochs+1):
        for batch in train_iter:
            feature = batch.text
            targets = [batch.HS, batch.TR, batch.AG]
            feature = feature.data.t()
            targets = [tgt.data.sub(1) for tgt in targets]  # batch first, index align
            #targets = [F.one_hot(tgt) for tgt in targets]
            target = torch.cat([tgt.unsqueeze(1) for tgt in targets], dim=1)#.unsqueeze(1)
            #target = torch.nn.functional.one_hot(target)
            if args.cuda:
                feature = feature.cuda()
                target = target.cuda()

            
            optimizer.zero_grad()
            logit = model(feature, targets[0])
            #loss = F.cross_entropy(logit[:,0], target)
            criterion = nn.CrossEntropyLoss()
            loss = criterion(logit, target)
            loss.backward()
            optimizer.step()

            steps += 1
            if steps % args.log_interval == 0:
                corrects = (torch.max(logit, 1)[1].view(target.size()).data == target.data).sum()
                accuracy = 100.0 * corrects/batch.batch_size / 3
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
                        #save(model, args.save_dir, 'best', steps)
                        #print(args.save_dir,"\n",steps)
                        save(model, "./cnn2/snapshot/", "best", "model")
                else:
                    if steps - last_step >= args.early_stop:
                        print('early stop by {} steps.'.format(args.early_stop))
            #elif steps % args.save_interval == 0:
            #    save(model, args.save_dir, './cnn/snapshot', steps)

"""

def test(data_iter, models, args):
    for model in models:
        model.eval()
    if args.test:
        torch.no_grad()
        precision = []
        recall = []
        f1 = []
        emr = 0
        tot = 0
    
    corrects, avg_loss = 0, 0
    for batch in data_iter:
        feature = batch.text
        targets = [batch.HS, batch.TR, batch.AG]
        feature = feature.data.t()
        targets = [tgt.data.sub(1) for tgt in targets]  # batch first, index align
        #targets = [F.one_hot(tgt) for tgt in targets]
        target = torch.cat([tgt.unsqueeze(1) for tgt in targets], dim=1)#.unsqueeze(1)
        #target = torch.nn.functional.one_hot(target)
        if args.cuda:
            feature = feature.cuda()
            target = target.cuda()

        HS = models[0](feature)
        TG = models[1](feature,HS)
        AG = models[2](feature,HS)
        outs = [HS,TG,AG]
        logit = torch.cat([out.unsqueeze(-1) for out in outs], dim=-1)#.squeeze(2)
        
        #loss = F.cross_entropy(logit[:,0], target)
        criterion = nn.CrossEntropyLoss()
        loss = criterion(logit, target)

        avg_loss += loss.item()
        corrects += (torch.max(logit, 1)
                     [1].view(target.size()).data == target.data).sum()
        
        
        ### NEW
        if args.test:
            output = logit.clone()#.cpu()
            predicted = torch.max(output, 1)[1]
            predicted = predicted.cpu()
            target = target.cpu()
            
            m0 = (predicted.data[:,0] == target.data[:,0])
            m1 = (predicted.data[:,1] == target.data[:,1])
            m2 = (predicted.data[:,2] == target.data[:,2])
            emr += (m0 & m1 & m2).sum()
            tot += len(m0)*1.0
            #predicted = predicted.numpy()
            #_, trues = torch.max(target, 1)
            #print(logit.shape)
            #print(target)
            #print(predicted.shape)
            p = [0,0,0]
            r = [0,0,0]
            f = [0,0,0]
            for i in range(3):
                p[i] = precision_score(y_true=target[:,i], y_pred=predicted[:,i], average='weighted')#, average='weighted')
                r[i] = recall_score(y_true=target[:,i], y_pred=predicted[:,i], average='weighted')
                f[i] = f1_score(y_true=target[:,i], y_pred=predicted[:,i], average='weighted')
            #print(p)
            precision.append(p)
            recall.append(r)
            f1.append(f)
       
    if args.test:
        precision = np.mean(np.array(precision),axis=0)
        recall = np.mean(np.array(recall),axis=0)
        f1 = np.mean(np.array(f1),axis=0)
        print(emr)
        emr = emr/tot

    size = len(data_iter.dataset)*3
    avg_loss /= size
    accuracy = 100.0 * corrects/size
    print('\nEvaluation - loss: {:.6f}  acc: {:.4f}%({}/{}) \n'.format(avg_loss, 
                                                                       accuracy, 
                                                                       corrects, 
                                                                       size))
    if args.results_path is not None:
        save_test(args, precision, recall, f1, accuracy, emr)
    
    return accuracy



def save_test(args, precision, recall, f1, accuracy, emr):
    with open(args.results_path,'w', encoding="utf8") as ff:
        for i,j in enumerate(["HS","TR","AG"]):
            string = j + "\nPrecision: {:.3f}\nRecall: {:.3f}\nF1-Score: {:.3f}\n".format(precision[i],recall[i],f1[i])
            print(string)
        
            ff.write(string)
            ff.write("Accuracy: {:.3f}\n".format(accuracy))
            
        gen_f1 = np.mean(f1)
        string = "Task2\nEMR: {:.3f}\nF1-Score(Macro): {:.3f}\n".format(emr,gen_f1)
        print(string)
        ff.write(string)
        
    #print(path)


def predict(text, model, text_field, label_feild, cuda_flag):
    assert isinstance(text, str)
    model.eval()
    # text = text_field.tokenize(text)
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
