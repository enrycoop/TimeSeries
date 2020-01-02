[General]
RandomSeed = 1
Verbose = 0

[Data]
File = resources/9/train5000.arff
TestSet = resources/9/test5000.arff

[Attributes]
Target = 3
Descriptive = 2,4-7

[Tree]
Heuristic = VarianceReduction

[Ensemble]
Iterations = 100
EnsembleMethod = RForest

[SemiSupervised]
UnlabeledData = resources/9/unlabeled5000.arff
SemiSupervisedMethod = PCT
InternalFolds = 3

[Output]
TrainErrors = Yes
TestErrors = Yes