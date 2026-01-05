## Mobile Games A/B Testing: Cookie Cats

#### Project overview
- This project analyzes the results of an A/B test conducted in the popular mobile puzzle game Cookie Cats, developed by **Tactile Entertainment**.
- The primary objective was to evaluate the impact on player retention when the game's two different game versions, those are gate_30 and gate_40. While installing the game, user was by defaulty
  added to the either gate_30 or gate_40 version.
- Our agenda is to test which version (either gate_30 or gate_40) of game is more engaging with the users even after 7 days of installing the game.

#### Problem Statement
- In this project our aim to check which version of Cookie Cats game mostly engaging with the user, even after 7 days of installing the game

#### About the dataset
- The dataset includes data from over 90,000 players, randomly assigned to either the gate_30 or gate_40 version of the game.
- **Columns**: userid, version, sum_gamerounds, retention_1, retention_7.

#### Methodology
- Check basic statistics about the data
- Perform the EDA
- Data cleaning and Handling outliers
- Statistical Hypothesis testing (Proportion Z-test)
- Bootstrapping to determine the certainty of the retention differences

#### Key Findings
- The analysis says Day 1 retention for gate_30 and gate_40 almost same, but when coming with the Day 7 retention comparing with the gate_40, gate_30 is engaging users more.
- We have checked with the Bootstrapping Confidence intervals and from these, we have seen gate_30 is engaging users more.

#### Conclusion
> Comparing with gate_40, gate_30 leads to more 7-day retention/stickiness (p=0.0016, CI=[0.003,0.013]).
  Day 1 shows borderline improvement (p=0.074). Recommend gate_30 for better long-term engagement.

#### **Source**
- This project is taken reference from the Kaggle notebook. Original Author for this project is **Ekrem Bayar**. Thanks to **Ekrem Bayar** sir.
original code notebook link from Kaggle: https://www.kaggle.com/code/ekrembayar/a-b-testing-step-by-step-hypothesis-testing/notebook
