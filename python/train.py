import torch
import numpy as np

from tqdm import tqdm


def train(device, num_strings, batch_size, 
          synt_net, rec_net, 
          criterion, optimizer, epochs, n):
    
    for epoch in tqdm(range(epochs)):
        running_loss = 0.0
        accuracy = torch.tensor([])
        
        for i in (range(int(num_strings / batch_size))):
            
            # generate batch with random bit strings
            input_bit_string_batch = torch.tensor(
                np.random.choice([-1, 1], size=(batch_size, n))
            ).to(device)
            
            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            synt_outputs = synt_net(input_bit_string_batch)
            rec_outputs = rec_net(synt_outputs)
            
            #print('input: ', input_bit_string_batch[0])
            #print('rec: ', torch.sign(rec_outputs[0]))
            
            # criterion = sigmoid
            # the loss is distributed between −1 (perfect recognition) and 0
            loss = torch.mean(-torch.mean(
                criterion(
                    input_bit_string_batch * rec_outputs
                ), axis=1
            ))
            
            # calculate accuracy
            accuracy = torch.cat([
                accuracy, torch.sum(
                    input_bit_string_batch == torch.sign(rec_outputs)
                    , axis=1)
            ])
            
            #print('loss', loss)
            loss.backward()
            
            optimizer.step()

            # print statistics
            running_loss += loss.item()

        print('Epoch: ', epoch + 1)
        print('Loss: ', running_loss)
        print('Mean accuracy: {}\n'.format(torch.mean(accuracy / n)))

