# REPORT

## 1. Data preparation
## 2. Data exploration
## 3. Data enrichment
## 4. Streaming

lets start with the Architecture of the pipeline .......
the live treatment pipeline is built on the continuous feeding of wikipedia pages modifications and their links with a IMDB reference. 

First, we use Kafka as a broker with a producer script  that listen the continuous public flow of recents wikipedia modifications and publish each events in wikipedia-changes. then our Spark motor, fed by this contnent link the title of each modificated pages with one of our reference tables from IMDB ( 24244 movies and 47899 personnas). To avoid the false positive, a filter analyse the () in the end of titel like we could have on Alien ( franchise). this process help us to avoid generic pages or homonymes. our validated links are then stocked in a 30 minutes sliding window ( with a 5 minutes jump ), as soon as a frame reach the critical points defined by --min-matches, it gets flagged. 

on our collect session that lasted 26 minutes, the pipeline recorded different metrics : first a global volume of 2190 events passed by KAFKA the only 63 events matched with our IDMB base ( 2.9%). those 63 events are divided in 2 categories : 28 are linked to personalities and about 35 are linked to movies. those 63 event reprensent 47 wikipedia pages. 

only 3 windows were written and all passed over the critical point :

18:25 - 18:55 : 15 matchs
18:30 - 19:00 : 27 matchs
18:35 - 19:05 : 40 matchs

we justify our kafak /spark methodology by two main reasons : 

First kafka act like a buffer between the data source and the calculus. if the spark treatment is interrupted or restrating, the messages are still conserved in kafka and the treatment restart exactly where the last offset was validated. 

the econd reason is more technical : Kafka is better in transport and flux retetion in high speed while spark have enough processing power for complex joins and aggregations. Furthermore, using Spark Structured Streaming makes it possible to use the same DataFrame API as for batch processing, facilitating the direct reuse of the IMDb tables prepared upstream.

we choosed a stream static - broadcast joint to avoid the shuffle. when we broadcast a full copy of IMDB on the memory f each worker node, each coming event is compared locally. this system avoid spark to redistribute all the data flow on the shuffle by joints keys. 

we also choosed sliding windows for 2 reason : 

Sliding windoxs are more interesting than tumbling windows ( who cut the time in blocs and can mask the A peak of activity if it straddles two intervals) because  the sliding window (30 minutes wide, 5-minute step) always assure a continuous coverage. 

we also choosed tge sliding windows for the accuracy because 1 same event could be considered in 6 windows that are working at the same time. even if this increase the work of the CPU to keep the windows active this way is way better to observe meticulously the evolution of trends and to set the flagged alarm as soon as the ccritical point is hit. 

we also choosed to put the watermark at 10 minutes because this timeframe is perfect to avoid loosing some data ! 
since the wikipedia flow is almost instant, a timeframe to short like 1 minute would make us loose all the data that is being slowed by the network and a timeframe too long ( 1 hour) would just delay unnecessarily the publication of results and increase memory usage.

to conclude this chapter lets analyze the 3 windows result : 
Only 3 windows have been opened : this is explained by the combination of the time of the first match, the position of the watermark, and the writing mode used:

on the Lower bound, The first IMDb match was recorded at 18:50:16. Any window ending before this time being empty, the first relevant window is the one covering 18:25 – 18:55

On the Upper bound and Append mode: The last event of the test was captured at 19:15:51, placing the final watermark around 19:05:51. In append output mode, Spark guarantees the immutability of results: it only writes a window once the watermark has strictly passed its end. Only the windows ending at 18:55, 19:00, and 19:05 met this condition at the time the pipeline stopped. The following windows (19:10, 19:15, etc.) were still waiting to close in memory.

But there is some limits to this exeriment :

on a windows of 26 minutes, the watermark blocks the export on the last minutes of activity. A longer execution time or a change in the update mode would make us able to observe more windows. 

the size of the sample is also too small : the analysis is done on a small batch of data that doesnt represent the general statistics on Wikipedia's overall activity.

and our last liimits is obviously the IMDb reference bias: Since the reference table is filtered to movies and personalities that received the most votes, the pipeline  ignores changes related to more rare or recent works, which partly explains the 2.9% match rate.

## 5. Open question
