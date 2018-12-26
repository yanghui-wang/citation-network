Introduction
This project creates a citation network from a data set of published paper and an importance ranking of the books. I used the Citation-network V1 dataset from https://aminer.org/citation for this project. The project in written in Python 2.7 and particular attention is paid to PageRank and virtualization of the results. The report includes pseudo-code that explains how the program works such that a Python programmer could read it and understand how to create the program from scratch. 

Description

•Data description: 
The Citation-network V1 data set is released in 2010-05-15 with 629,814 papers and >632,752 citation relationships. It is organized into ~600,000 blocks, each for a paper. For each block, each line starting with a specific prefix indicates an attribute of the paper. 

•Outline Solution and Design:
a.Data Cleaning: 
1.Import the original data and separate them into corresponding columns for further operations using re package.
2.Create lists and strings containing relevant information by extracting from the data frame above.

b.Create Network:
1.Every paper is a unique node, and in this case, there are 629814 nodes in total.
2.Create a directed connection from paper A to B if paper A cited paper B. 

c.Ranking: 
We rank the paper by importance with PageRank algorithm, which works by counting the number and quality of citation to a paper to determine a rough estimate of how important the paper is. The underlying assumption is that more important papers are likely to receive more citations from other papers. In this project, we define most important as the node with the highest page rank score and set the damping factor to 0.99, assuming that the importance of paper is almost solely determined by citation.

d.Virtualization: 

Part I: Network Graph
Since the whole network contains a huge amount of data, it is not possible to visualize all the information in a clean and nice way. For the purpose of a visually pleasing picture, we decided to visualize only some of the important nodes. We first tried to extract the most important 30 papers in the whole dataset, but unfortunately there is no connected edge among them. In order to make sure the network is at least connected, we came up with a different way of selecting important papers. Starting from the most important paper, we find the papers that cited it and virtualize the first 20 most important ones. Within this citation subgroup, we continue the step until no more papers cited the most important paper in the subgroup. In this case, we determined the importance of the paper by their page rank score within the whole dataset. The graph is built with networkx and matplotlib.pyplot. 

Part II: Rank Table with Distribution Graph 
Besides the PageRank algorithm, we also think it important to rank the papers by the number of times they were cited. This not only helps people to look at the data from a different perspective, but also functions to verify the result of page rank score. This is done by using the prettytable and ntlk package. 

Conclusion
From the virtualization, one can see that the size of the node is related to the importance rank of the node. In general, as the center node of each cluster becomes less important, the number of nodes pointed to it becomes smaller and the nodes are less important in trend. The result quite matches with the result in theory, since in our page rank algorithm, the paper that gets cited most often should be of very high importance. On the other hand, if the importance rank of a paper is low it usually means fewer papers cited this paper in this network.

Reference
Jie Tang, Jing Zhang, Limin Yao, Juanzi Li, Li Zhang, and Zhong Su. ArnetMiner: Extraction and Mining of Academic Social Networks. In Proceedings of the Fourteenth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (SIGKDD'2008). pp.990-998. [PDF] [Slides] [System] [API]
Jie Tang, Limin Yao, Duo Zhang, and Jing Zhang. A Combination Approach to Web User Profiling. ACM Transactions on Knowledge Discovery from Data (TKDD), (vol. 5 no. 1), Article 2 (December 2010), 44 pages.  [PDF]
Jie Tang, A.C.M. Fong, Bo Wang, and Jing Zhang. A Unified Probabilistic Framework for Name Disambiguation in Digital Library. IEEE Transaction on Knowledge and Data Engineering (TKDE), Volume 24, Issue 6, 2012, Pages 975-987. [PDF][Code&Data&System]
Jie Tang, Jing Zhang, Ruoming Jin, Zi Yang, Keke Cai, Li Zhang, and Zhong Su. Topic Level Expertise Search over Heterogeneous Networks. Machine Learning Journal, Volume 82, Issue 2 (2011), Pages 211-237. [PDF] [URL]
Jie Tang, Duo Zhang, and Limin Yao. Social Network Extraction of Academic Researchers. In Proceedings of 2007 IEEE International Conference on Data Mining(ICDM'2007). pp. 292-301. [PDF] [Slides] [Data]
Arnab Sinha, Zhihong Shen, Yang Song, Hao Ma, Darrin Eide, Bo-June (Paul) Hsu, and Kuansan Wang. 2015. An Overview of Microsoft Academic Service (MAS) and Applications. In Proceedings of the 24th International Conference on World Wide Web (WWW ’15 Companion). ACM, New York, NY, USA, 243-246. [PDF][System]

