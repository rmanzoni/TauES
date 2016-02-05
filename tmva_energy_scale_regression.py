import ROOT
from ROOT import TMVA


# Logon not automatically loaded through PyROOT (logon loads TMVA library) load also GUI
ROOT.gROOT.SetMacroPath( './' )
ROOT.gROOT.Macro       ( './TMVAlogon.C' )    
ROOT.gROOT.LoadMacro   ( './TMVAGui.C' )

outfname = 'TMVAReg.root'
f_out = ROOT.TFile.Open( outfname, 'recreate' )

# Create the factory object. Later you can choose the methods
# whose performance you'd like to investigate. The factory will
# then run the performance analysis for you.
#
# The first argument is the base of the name of all the
# weightfiles in the directory weight/ 
#
# The second argument is the output file for the training results
# All TMVA output can be suppressed by removing the '!' (not) in 
# front of the 'Silent' argument in the option string
factory = TMVA.Factory( 'TMVARegression', f_out, '!V:!Silent:Color:DrawProgressBar' )

# Set verbosity
factory.SetVerbose( True )


# Define the input variables that shall be used for the classifier training
# note that you may also use variable expressions, such as: '3*var1/var2*abs(var3)'
# [all types of expressions that can also be parsed by TTree::Draw( 'expression' )]
# factory.AddVariable( 'tau_pt'       , 'F' )
# factory.AddVariable( 'tau_eta'      , 'F' )
# factory.AddVariable( 'tau_mass'     , 'F' )
# factory.AddVariable( 'tau_decayMode', 'I' )
factory.AddVariable( 'tau_pt'                           , 'F' )
factory.AddVariable( 'tau_eta'                          , 'F' )
factory.AddVariable( 'tau_mass'                         , 'F' )
factory.AddVariable( 'tau_decayMode'                    , 'I' )
 
factory.AddVariable( 'tau_lead_charged_pt'              , 'F' )
factory.AddVariable( 'tau_lead_neutral_pt'              , 'F' )

factory.AddVariable( 'tau_charged_iso'                  , 'F' )
factory.AddVariable( 'tau_gamma_iso'                    , 'F' )
factory.AddVariable( 'tau_neutral_iso'                  , 'F' )
factory.AddVariable( 'tau_charged_sig'                  , 'F' )
factory.AddVariable( 'tau_gamma_sig'                    , 'F' )
factory.AddVariable( 'tau_neutral_sign'                 , 'F' )
 
factory.AddVariable( 'tau_jet_pt'                       , 'F' )
factory.AddVariable( 'tau_jet_mass'                     , 'F' )
factory.AddVariable( 'tau_jet_nConstituents'            , 'F' )
factory.AddVariable( 'tau_jet_rawFactor'                , 'F' )
factory.AddVariable( 'tau_jet_chargedHadronEnergy'      , 'F' )
factory.AddVariable( 'tau_jet_neutralHadronEnergy'      , 'F' )
factory.AddVariable( 'tau_jet_neutralEmEnergy'          , 'F' )
factory.AddVariable( 'tau_jet_chargedEmEnergy'          , 'F' )
factory.AddVariable( 'tau_jet_chargedHadronMultiplicity', 'F' )
factory.AddVariable( 'tau_jet_neutralMultiplicity'      , 'F' )

# factory.AddVariable( 'tau_puCorrPtSum'                 , 'F' )
# factory.AddVariable( 'tau_photonPtSumOutsideSignalCone', 'F' )
# factory.AddVariable( 'tau_footprintCorrection'         , 'F' )
# factory.AddVariable( 'tau_chargedIsoPtSum'             , 'F' )

# Add the variable carrying the regression target
# factory.AddTarget( 'tau_gen_vis_pt' )
factory.AddTarget( 'tau_gen_vis_pt' )

# Open input file
# f_in  = ROOT.TFile.Open( 'tree.root' )
f_in  = ROOT.TFile.Open( 'total_tree.root' )
# Register the regression tree
regTree = f_in.Get( 'tree' )
# global event weights per tree (see below for setting event-wise weights
regWeight  = 1.

# You can add an arbitrary number of regression trees
factory.AddRegressionTree(regTree, regWeight)

# Apply additional cuts on the signal and background sample. 
# example for cut: mycut = TCut( 'abs(var1)<0.5 && abs(var2-0.5)<1' )
# mycut = ROOT.TCut('abs(tau_gen_pdgId) == 15  && tau_gen_vis_pt > 0.') 
# mycut = ROOT.TCut('tau_jet_mass > 0. & abs(tau_gen_pdgId) == 15  && tau_gen_vis_pt > 0. & tau_byCombinedIsolationDeltaBetaCorr3Hits >= 0 & tau_gen_vis_pt < 1000.') 
# mycut = ROOT.TCut('tau_jet_mass > 0. & abs(tau_gen_pdgId) == 15  && tau_gen_vis_pt > 0. & tau_byCombinedIsolationDeltaBetaCorr3Hits >= 0 & tau_gen_vis_pt < 1000. & tau_decayMode == 0') 
# mycut = ROOT.TCut('tau_jet_mass > 0. & abs(tau_gen_pdgId) == 15  && tau_gen_vis_pt > 0. & tau_byCombinedIsolationDeltaBetaCorr3Hits >= 0 & tau_gen_vis_pt < 1000. & tau_decayMode == 1') 
# mycut = ROOT.TCut('tau_jet_mass > 0. & abs(tau_gen_pdgId) == 15  && tau_gen_vis_pt > 0. & tau_byCombinedIsolationDeltaBetaCorr3Hits >= 0 & tau_gen_vis_pt < 1000. & tau_decayMode == 10') 
# mycut = ROOT.TCut('tau_jet_mass > 0. & abs(tau_gen_pdgId) == 15  && tau_gen_vis_pt > 0. & tau_byCombinedIsolationDeltaBetaCorr3Hits >= 0 & tau_gen_vis_pt < 1000. & tau_decayMode != 0 & tau_decayMode != 1 & tau_decayMode != 10') 

mycut = ROOT.TCut(
'abs(tau_gen_pdgId) == 15  & \
tau_gen_vis_pt                            >  0. &\
tau_byCombinedIsolationDeltaBetaCorr3Hits >= 0  &\
tau_pt                                    >  0. &\
tau_mass                                  >  0. &\
tau_decayMode                             >= 0. &\
tau_lead_charged_pt                       >= 0. &\
tau_charged_iso                           >= 0. &\
tau_gamma_iso                             >= 0. &\
tau_neutral_iso                           >= 0. &\
tau_charged_sig                           >= 0. &\
tau_gamma_sig                             >= 0. &\
tau_neutral_sign                          >= 0. &\
tau_jet_pt                                >= 0. &\
tau_jet_mass                              >= 0. &\
tau_jet_nConstituents                     >= 0. &\
tau_jet_rawFactor                         >= 0. &\
tau_jet_chargedHadronEnergy               >= 0. &\
tau_jet_neutralHadronEnergy               >= 0. &\
tau_jet_neutralEmEnergy                   >= 0. &\
tau_jet_chargedEmEnergy                   >= 0. &\
tau_jet_chargedHadronMultiplicity         >= 0. &\
tau_jet_neutralMultiplicity               >= 0.') 


# tell the factory to use all remaining events in the trees after training for testing:
factory.PrepareTrainingAndTestTree( 
    mycut, 
    ':'.join([
        'nTrain_Regression=10000',
        'nTest_Regression=10000',
        'SplitMode=Random',
        'NormMode=NumEvents',
        '!V'
    ]) 
)
#     factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG"+postfix, "!H:!V:NTrees=500::BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.9:nCuts=500:MaxDepth=4:MinNodeSize=10" )
# 
# 
#     # factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_TOP", "!H:!V:NTrees=400:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=50:AdaBoostBeta=0.005:MaxDepth=5")
#     # Optimizerd:
#     factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_TOP"+postfix, "!H:!V:NTrees=400 :BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=50:AdaBoostBeta=0.2:MaxDepth=2:MinNodeSize=6")
#     factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG"           , "!H:!V:NTrees=250 :BoostType=Grad    :Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.9:nCuts=500:MaxDepth=4:MinNodeSize=5" )
#     factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG"           , "!H:!V:NTrees=250 :BoostType=Grad    :Shrinkage=0.275:UseBaggedBoost:GradBaggingFraction=0.9:nCuts=500:MaxDepth=2:MinNodeSize=15" )
#     factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG"           , "!H:!V:NTrees=1000:BoostType=Grad    :Shrinkage=0.5:UseBaggedBoost:GradBaggingFraction=0.9:nCuts=500:MaxDepth=2:MinNodeSize=1" )



# Boosted Decision Trees
# factory.BookMethod( 
#     TMVA.Types.kBDT, 
#     'BDT',
#     ':'.join([
#         '!H',
#         'V',
#         'NTrees=300',
#         'MinNodeSize=0.35',
#         'MaxDepth=3',
#         'BoostType=AdaBoostR2',
#         'SeparationType=RegressionVariance',
#         'nCuts=10000',
#         'PruneMethod=NoPruning',
#     ])
# )
# 
# 
# factory.BookMethod( 
#     TMVA.Types.kBDT, 
#     'BDT-1',
#     ':'.join([
#         '!H',
#         'V',
#         'NTrees=1000',
#         'MinNodeSize=0.35',
#         'MaxDepth=3',
#         'BoostType=AdaBoostR2',
#         'SeparationType=RegressionVariance',
#         'nCuts=1000',
#         'PruneMethod=CostComplexity',
#         'PruneStrength=10',
#     ])
# )
# 
# factory.BookMethod( 
#     TMVA.Types.kBDT, 
#     'BDT-2',
#     ':'.join([
#         '!H',
#         'V',
#         'NTrees=1000',
#         'MinNodeSize=0.35',
#         'MaxDepth=3',
#         'BoostType=AdaBoostR2',
#         'SeparationType=RegressionVariance',
#         'nCuts=1000',
#         'UseFisherCuts',
#         'PruneMethod=CostComplexity',
#         'PruneStrength=10',
#     ])
# )
# 
# 
# 
# factory.BookMethod(
#     TMVA.Types.kBDT, 
#     'BDT-3',
#     ':'.join([
#         '!H',
#         '!V',
#         'NTrees=100',
#         'MinNodeSize=1.0%',
#         'BoostType=AdaBoostR2',
#         'SeparationType=RegressionVariance',
#         'nCuts=20',
#         'PruneMethod=CostComplexity',
#         'PruneStrength=30'
#     ])
# )

# factory.BookMethod(
#     TMVA.Types.kBDT, 
#     'BDT-4',
#     ':'.join([
#         '!H',
#         'V',
#         'NTrees=10000',
#         'MinNodeSize=0.4',
#         'MaxDepth=10',
#         'BoostType=AdaBoostR2',
#         'SeparationType=RegressionVariance',
#         'nCuts=100',
#         'PruneMethod=NoPruning',
#     ])
# )


# factory.BookMethod(
#     TMVA.Types.kBDT, 
#     'BDT-5',
#     ':'.join([
#         '!H',
#         'V',
#         'NTrees=100',
#         'MinNodeSize=0.4',
#         'MaxDepth=3',
#         'BoostType=AdaBoostR2',
#         'SeparationType=RegressionVariance',
#         'nCuts=1000',
#         'PruneMethod=NoPruning',
#     ])
# )


# factory.BookMethod(
#     TMVA.Types.kBDT, 
#     'BDT-6',
#     ':'.join([
#         '!H',
#         'V',
#         'NTrees=10000',
#         'MinNodeSize=0.4',
#         'MaxDepth=2',
#         'BoostType=AdaBoostR2',
#         'SeparationType=RegressionVariance',
#         'nCuts=100',
#         'PruneMethod=CostComplexity',
#         'PruneStrength=10'
#     ])
# )

# factory.BookMethod(
#     TMVA.Types.kBDT, 
#     'BDT-7',
#     ':'.join([
#         '!H',
#         '!V',
#         'NTrees=100',
#         'MinNodeSize=.4%',
#         'BoostType=AdaBoostR2',
#         'SeparationType=RegressionVariance',
#         'nCuts=100',
#         'PruneMethod=CostComplexity',
#         'PruneStrength=20'
#     ])
# )
# 
# factory.BookMethod(
#     TMVA.Types.kBDT, 
#     'BDT-8',
#     ':'.join([
#         '!H',
#         '!V',
#         'NTrees=100',
#         'MinNodeSize=0.4%',
#         'BoostType=AdaBoostR2',
#         'SeparationType=RegressionVariance',
#         'MaxDepth=3',
#         'nCuts=20',
#         'PruneMethod=CostComplexity',
#         'PruneStrength=10'
#     ])
# )
# 
# factory.BookMethod( 
#     TMVA.Types.kBDT, 
#     'BDTG-1',
#     ':'.join([
#         'H',
#         'V',
#         'NTrees=1000',
#         '',
#         'BoostType=Grad',
#         'Shrinkage=0.1',
#         'UseBaggedBoost',
#         'BaggedSampleFraction=0.5',
#         'nCuts=500',
#         'MaxDepth=3',
#         'MinNodeSize=0.4',
#     ])
# )

# factory.BookMethod( 
#     TMVA.Types.kBDT, 
#     'BDTG-2',
#     ':'.join([
#         'H',
#         'V',
#         'NTrees=2000',
#         '',
#         'BoostType=Grad',
#         'Shrinkage=0.1',
#         'UseBaggedBoost',
#         'BaggedSampleFraction=0.5',
#         'nCuts=1000',
#         'MaxDepth=4',
#         'MinNodeSize=0.4',
#         'PruneMethod=CostComplexity',
#         'PruneStrength=10'
#     ])
# )
# 
# factory.BookMethod( 
#     TMVA.Types.kBDT, 
#     'BDTG-3',
#     ':'.join([
#         'H',
#         'V',
#         'NTrees=2000',
#         '',
#         'BoostType=Grad',
#         'Shrinkage=0.1',
#         'UseBaggedBoost',
#         'BaggedSampleFraction=0.5',
#         'nCuts=1000',
#         'MaxDepth=4',
#         'MinNodeSize=0.4',
#         'PruneMethod=NoPruning',
#     ])
# )


# factory.BookMethod( 
#     TMVA.Types.kBDT, 
#     'BDTG-4',
#     ':'.join([
#         'H',
#         'V',
#         'NTrees=500',
#         '',
#         'BoostType=Grad',
#         'Shrinkage=0.1',
#         'UseBaggedBoost',
#         'BaggedSampleFraction=0.5',
#         'nCuts=2000',
#         'MaxDepth=4',
#         'MinNodeSize=0.3',
#         'PruneMethod=CostComplexity',
#         'PruneStrength=10'
#     ])
# )

# factory.BookMethod( 
#     TMVA.Types.kBDT, 
#     'BDTG-5',
#     ':'.join([
#         'H',
#         'V',
#         'NTrees=5000',
#         '',
#         'BoostType=Grad',
#         'Shrinkage=0.1',
#         'UseBaggedBoost',
#         'BaggedSampleFraction=0.5',
#         'nCuts=2000',
#         'MaxDepth=4',
#         'MinNodeSize=0.3',
#         'PruneMethod=CostComplexity',
#         'PruneStrength=10'
#     ])
# )

# factory.BookMethod(
#     TMVA.Types.kBDT, 
#     'BDTG-6',
#     ':'.join([
#         'H',
#         'V',
#         'NTrees=400',
#         '',
#         'BoostType=Grad',
#         'Shrinkage=0.1',
#         'UseBaggedBoost',
#         'BaggedSampleFraction=0.5',
#         'nCuts=100',
#         'MaxDepth=100',
#         'MinNodeSize=0.4',
#         'PruneMethod=CostComplexity',
#         'PruneStrength=30'
#     ])
# )

# factory.BookMethod(
#     TMVA.Types.kBDT, 
#     'BDTG-7',
#     ':'.join([
#         'H',
#         'V',
#         'NTrees=4000',
#         '',
#         'BoostType=Grad',
#         'Shrinkage=0.3',
#         'UseBaggedBoost',
#         'BaggedSampleFraction=0.5',
#         'nCuts=200',
#         'MaxDepth=6',
#         'MinNodeSize=0.3',
#         'PruneMethod=CostComplexity',
#         'PruneStrength=10'
#     ])
# )




# factory.BookMethod(
#     TMVA.Types.kBDT, 
#     'BDTG-8',
#     ':'.join([
#         'H',
#         'V',
#         'NTrees=5000',
#         '',
#         'BoostType=Grad',
#         'Shrinkage=0.3',
#         'UseBaggedBoost',
#         'BaggedSampleFraction=0.5',
#         'nCuts=600',
#         'MaxDepth=30',
#         'MinNodeSize=0.2',
#         'PruneMethod=CostComplexity',
#         'PruneStrength=40'
#     ])
# )

factory.BookMethod(
    TMVA.Types.kBDT, 
    'BDTG-8',
    ':'.join([
        'H',
        'V',
        'NTrees=10000',
        '',
        'BoostType=Grad',
        'Shrinkage=0.1',
        'UseBaggedBoost',
        'BaggedSampleFraction=0.5',
        'nCuts=1000',
        'MaxDepth=100',
        'MinNodeSize=0.2',
    ])
)


# Linear discriminant
# factory.BookMethod( 
#     TMVA.Types.kLD, 
#     'LD',
#     ':'.join([
#         '!H',
#         '!V',
#         'VarTransform=None' 
#     ])
# )



# factory.BookMethod( 
#     TMVA.Types.kBDT, 
#     'BDTG-DM0',
#     ':'.join([
#         'H',
#         'V',
#         'NTrees=1000',
#         '',
#         'BoostType=Grad',
#         'Shrinkage=0.1',
#         'UseBaggedBoost',
#         'BaggedSampleFraction=0.5',
#         'nCuts=500',
#         'MaxDepth=3',
#         'MinNodeSize=0.4',
#     ])
# )
# factory.BookMethod( 
#     TMVA.Types.kBDT, 
#     'BDTG-DM1',
#     ':'.join([
#         'H',
#         'V',
#         'NTrees=1000',
#         '',
#         'BoostType=Grad',
#         'Shrinkage=0.1',
#         'UseBaggedBoost',
#         'BaggedSampleFraction=0.5',
#         'nCuts=500',
#         'MaxDepth=3',
#         'MinNodeSize=0.4',
#     ])
# )
# factory.BookMethod( 
#     TMVA.Types.kBDT, 
#     'BDTG-DM10',
#     ':'.join([
#         'H',
#         'V',
#         'NTrees=1000',
#         '',
#         'BoostType=Grad',
#         'Shrinkage=0.1',
#         'UseBaggedBoost',
#         'BaggedSampleFraction=0.5',
#         'nCuts=500',
#         'MaxDepth=3',
#         'MinNodeSize=0.4',
#     ])
# )
# factory.BookMethod( 
#     TMVA.Types.kBDT, 
#     'BDTG-DMother',
#     ':'.join([
#         'H',
#         'V',
#         'NTrees=1000',
#         '',
#         'BoostType=Grad',
#         'Shrinkage=0.1',
#         'UseBaggedBoost',
#         'BaggedSampleFraction=0.5',
#         'nCuts=500',
#         'MaxDepth=3',
#         'MinNodeSize=0.4',
#     ])
# )
# 
# ---- Now you can tell the factory to train, test, and evaluate the MVAs

# Train MVAs using the set of training events
factory.TrainAllMethods()

# ---- Evaluate all MVAs using the set of test events
factory.TestAllMethods()

# ----- Evaluate and compare performance of all configured MVAs
factory.EvaluateAllMethods()

# --------------------------------------------------------------

# Save the output
f_out.Close()
   
# open the GUI for the result macros    
# ROOT.gROOT.ProcessLine( "TMVAGui(\"%s\")" % outfname )
TMVA.TMVARegGui(outfname)
# keep the ROOT thread running
ROOT.gApplication.Run() 


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
