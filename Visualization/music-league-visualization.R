# Music League Visualizations
# Author: Spencer Simon

###############################################################################
### Initialize Packages
library(circlize)

###############################################################################
### Load Data
dataPath <- "/Users/spencersimon/Documents/Projects/Coding/music-league-analysis"
chord.dat.20 <- read.csv(paste(dataPath,'SQL/SQL-Chord-20.csv',sep = '/'), header=TRUE)

###############################################################################
### Chord Diagram: Static
# Create adjacency list from SQL data and convert to matrix
chord.adj.list <- cbind(chord.dat.20[1], chord.dat.20[5], chord.dat.20[3])
chord.mat <- adjacencyList2Matrix(chord.adj.list)
chord.mat <- chord.mat[order(chord.mat[,1],decreasing=TRUE),]

chord.adj.top9 <- chord.adj.list[-127:-134,]
chord.adj.top9 <- chord.adj.top9[-109:-114,]
chord.adj.top9 <- chord.adj.top9[-92:-99,]
chord.adj.top9 <- chord.adj.top9[-12:-20,]
chord.mat.9 <- adjacencyList2Matrix(chord.adj.top9)
chord.mat.9 <- chord.mat.9[,-8:-9]
chord.mat.9 <- chord.mat.9[,-9]
chord.mat.9 <- chord.mat.9[,-10]

chord.mat.8 <- chord.mat.9[-8,]
chord.mat.8 <- chord.mat.8[,-8]

# Reorder chord.mat.8
rownames(chord.mat.8) <- c("Memory", "Tristan", "Spencer", "Nina", "Jon",
                           "Jayden", "Hunter", "Charles")
colnames(chord.mat.8) <- c("Nina", "Charles", "Jayden", "Spencer", "Tristan",
                           "Hunter", "Jon", "Memory")
col.order <- c(rownames(chord.mat.8))
chord.mat.8 <- chord.mat.8[,col.order]

chordDiagram(chord.mat, grid.col = 1:13, directional = 1, row.col = 1:13)
chordDiagram(chord.mat.8, grid.col = 1:8, directional = 1, row.col = 1:8)

###############################################################################
### Chord Diagram: Interactive
# Load package
#devtools::install_github("mattflor/chorddiag")
library(chorddiag)

# Data is chord.mat from above

# A vector of 13 colors for 13 groups
#dimnames(chord.mat) <- list(voter = haircolors,
 #                           voted_for = haircolors)
groupColors <- c("#010202", "#EE2E30", "#FFDE83", "#008C48", "#929292", 
                 "#185AA9", "#F47D23", "#662B91", "#C4E04D", 
                 "#A21D22", "#68DFCF", "#B43894", "#E5D826")

groupColors <- c("#010202", "#EE2E30", "#FFDE83", "#008C48", 
                 "#185AA9", "#F47D23", "#662B91", "#C4E04D")
                 #"#A21D22", "#68DFCF", "#B43894", "#E5D826")

# Build the chord diagram:
p <- chorddiag(chord.mat.8, #type = "bipartite", 
               groupColors = groupColors, groupnamePadding = 20)
p

# save the widget
library(htmlwidgets)
saveWidget(p, file=paste0( dataPath, "/chord_interactive.html"))
# 
