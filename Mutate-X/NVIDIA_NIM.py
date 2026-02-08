import requests
import os
import json
from pathlib import Path
import math
import csv
""""""
# Used to obtain ground truth data from the chosen ClinVar dataset.
def get_ground_truth():
    clinvar_dataset = Path("your_raw_data.csv")
    data = Path("./data.json")
    data_ = {}
    with open(clinvar_dataset, 'r', newline="") as f, open(data, 'w') as j:
            reader = csv.reader(f)
            head = next(reader)
            for row in reader:
                if row[-1] == "Pathogenic":
                    data_[row[0] + '+' + row[1]] = 1.00
        
                elif row[-1] == "Benign":
                    data_[row[0] + '+' + row[1]] = 0.00

                elif row[-1] == "Likely_pathogenic":
                    data_[row[0] + '+' + row[1]] = 0.75

                elif row[-1] == "Likely_benign":
                    data_[row[0] + '+' + row[1]] = 0.25

                elif row[-1] in ["Likely_pathogenic/Likely_benign","Likely_benign/Likely_pathogenic"]: #prefernce goes to likely pathogenic
                    data_[row[0] + '+' + row[1]] = 0.75

                elif row[-1] in ["Pathogenic/Likely_pathogenic", "Likely_pathogenic/Pathogenic"]: #prefernce goese to pathogenic
                    data_[row[0] + '+' + row[1]] = 1.00

                elif row[-1] in ["Benign/Likely benign", "Likely_benign/Benign"]: #prefernce goes to likely benign
                    data_[row[0] + '+' + row[1]] = 0.25
                
            json.dump(data_, j, indent=4)            
  
""""""
#Used to obtain the NVIDIA serverless processing API key from the environment.
api_key = os.getenv("NVIDIA_KEY")
print("API key loaded:", api_key is not None)

"""
To set an environment variable, follow these steps:

1. Open the terminal or a cmd prompt.

2. Use:
    - For Windows:
        setx NVIDIA_KEY "your-api_key"
    - For Linux/Mac:
        export NVIDIA_KEY="your-api_key"

3. Restart the terminal or cmd prompt to apply the changes.
"""

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

sequence = ["AGCCCCACCTACCTCTCCTCCT", "AGCCCCACCTTCCTCTCCTCCT"]
results = list()
for s in sequence:
    r = requests.post(
        url="https://health.api.nvidia.com/v1/biology/arc/evo2-40b/generate",
        headers=headers,
        json={
            "sequence": s,
            "num_tokens": 22,
            "top_k": 1,
            "enable_sampled_probs": True,
        },
    )
    if r.status_code != 200:
        print("Error:", r.status_code, r.text)
        break
    results.append(r.json()["sampled_probs"])


"""
results[0] → probability for REF
results[1] → probability for ALT
"""

"""
Using two different sequences, one with SNP mutation and another without mutation,
we get the log probabilities of each token in the sequence.
With one being ref: Refernce without mutation.
Another being alt: ALternate with mutation.
"""

def compute_delta():
    holder = list()
    for _ in range(0, 2):
        summ = 0.0
        probs = results[_]
        for p in probs:
            log_p = math.log(p)
            summ += log_p
        holder += [summ]

    delta = holder[1] - holder[0]
    return delta

"""
Delta is the difference between the probabilities of sequences when one neucleotide is mutated against that of the original sequence.
Now these probabilities are the summation of log probabilities of each token in the sequence.
"""

if __name__ == "__main__":
    print('Delta prbability is:', compute_delta())

## TO DO: Download the complete sequences, extracted the required region, create the mutated and normal sequences, pass them to the API and get the delta scores for evaluation.
## And calculate PR-AUC, ROC-AUC, Specificity, Sensitivity and Accuracy against the ground truth data and then we'll partly be done.
## Following that we need to compare it against SIFT and write the report.
