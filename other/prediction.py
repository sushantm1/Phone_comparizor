import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the model and tokenizer
model = load_model('nextword1.h5')
tokenizer = pickle.load(open('tokenizer1.pkl', 'rb'))

max_sequence_len = model.input_shape[1]  # Get max sequence length from the model

def Predict_Next_Words(model, tokenizer, text):
    """
    Predicts the next word for a given input sequence using a trained model.
    """
    for _ in range(3):  # Predict up to 3 words
        sequence = tokenizer.texts_to_sequences([text])[0]
        sequence = pad_sequences([sequence], maxlen=max_sequence_len-1, padding='pre')  # Pad sequence

        preds = model.predict(sequence, verbose=0)
        predicted_index = np.argmax(preds, axis=-1)[0]

        output_word = ''
        for word, index in tokenizer.word_index.items():
            if index == predicted_index:
                output_word = word
                break

        text += ' ' + output_word
        print(output_word)
    return output_word

# Main loop
while True:
    text = input("Enter your line: ")
    
    if text.lower().strip() == "stop the script":
        print("Ending The Program.....")
        break

    try:
        Predict_Next_Words(model, tokenizer, text)
    except Exception as e:
        print(f"Error: {e}")
        continue