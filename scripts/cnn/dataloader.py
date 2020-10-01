# A dataloader for importing CSV files to torchtext
# from https://gist.github.com/ohmeow/5b3543a5115040001fce59a105ac4269

import torchtext
import torch
from torchtext import data

class TextMultiLabelDataset(torchtext.data.Dataset):
    def __init__(self, df, tt_text_field, tt_label_field, txt_col, lbl_cols=["label"], **kwargs):
        # torchtext Field objects
        fields = [('text', tt_text_field)]
        for l in lbl_cols: fields.append((l, tt_label_field))
            
        is_test = False if lbl_cols[0] in df.columns else True
        n_labels = len(lbl_cols)
        
        examples = []
        for idx, row in df.iterrows():
            if not is_test:
                lbls = [ row[l] for l in lbl_cols ]
            else:
                lbls = [0.0] * n_labels
                
            txt = str(row[txt_col])
            examples.append(data.Example.fromlist([txt]+lbls, fields))
                            
        super().__init__(examples, fields, **kwargs)

    @staticmethod
    def sort_key(example): 
        return len(example.text)
    
    @classmethod
    def splits(cls, text_field, label_field, train_df, txt_col, lbl_cols=["label"], val_df=None, test_df=None, **kwargs):
        # build train, val, and test data
        train_data, val_data, test_data = (None, None, None)
        
        if train_df is not None: 
            train_data = cls(train_df.copy(), text_field, label_field, txt_col, lbl_cols, **kwargs)
        if val_df is not None: 
            val_data = cls(val_df.copy(), text_field, label_field, txt_col, lbl_cols, **kwargs)
        if test_df is not None: 
            test_data = cls(test_df.copy(), text_field, label_field, txt_col, lbl_cols, **kwargs)

        return tuple(d for d in (train_data, val_data, test_data) if d is not None)
    
