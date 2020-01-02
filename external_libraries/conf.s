[General]
Verbose = 0

[Data]
File = trans2.arff

[Attributes]
Target = 5
Descriptive = 2-4,6,7
Disable = 1
Weights = Normalize

[Tree]
Heuristic = GainRatio

[Ensemble]
Iterations = 100
EnsembleMethod = RForest

[SemiSupervised]
SemiSupervisedMethod = PCT
InternalFolds = 3

[Output]
TrainErrors = Yes
TestErrors = Yes