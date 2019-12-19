[General]
RandomSeed = 1
Verbose = 0

[Data]
File = resources/train25.arff
TestSet = resources/test25.arff

[Attributes]
Target = 3
Descriptive = 2,4-7
Key = 1

[Tree]
Heuristic = VarianceReduction
FTest = [0.001,0.005,0.01,0.05,0.1,0.125]
BinarySplit = No

[Ensemble]
Iterations = [5,100]
EnsembleMethod = RForest
VotingType = ProbabilityDistribution
SelectRandomSubspaces = LOG
FeatureRanking = RForest
WriteEnsemblePredictions = No

[SemiSupervised]
UnlabeledData = resources/unlabeled25.arff
SemiSupervisedMethod = PCT
Normalization = Standardization
InternalFolds = 3
ConfidenceThreshold = 0.8

[Output]
TrainErrors = Yes
TestErrors = Yes
WriteErrorFile = Yes
OutputPythonModel = No
AllFoldModels = No
ShowInfo = Key


