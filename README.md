# Overview

For this project I wanted to learn how to analyze a real dataset rather than build an application around one. My previous projects stored and retrieved data, and I became curious about what you can actually learn from data once it is collected.

The dataset is the National Park Service's visitor use statistics: monthly visitation counts for every NPS unit from 1979 through 2025. The raw file holds 2.9 million rows, one per unit, year, month, and statistic, covering fifteen different measures including recreation visits, visitor hours, and overnight stays. I obtained it from the NPS Stats database at https://irma.nps.gov/Stats/ and downloaded it on 11/17/2026.


[Software Demo Video](http://youtube.link.goes.here)

# Data Analysis Results

**Question 1: What is the best month to visit each National Park?**

I defined "best" as the quietest usable month. A month counts as usable if its average visits are at least 25% of the park's peak month; anything below that I treat as closed, so a park cannot win simply for being snowed in. Among the usable months, the best one is the quietest.

The answer is that **autumn wins**. September is the best month for 12 of the 64 parks, October for 10, and November for 9 — nearly half the park system falls in that three-month window. 

The most seasonal parks are all in Alaska or the northern Rockies, and they have only three or four usable months: For those parks the advice collapses to "go in September or not at all." Desert parks run the opposite way, with summer as the month to avoid and winter perfectly usable.

**Question 2: Which parks have grown or declined in popularity?**

I compared each park's average annual visits over its first three complete years against its last three, using only years with all twelve months of data.

**54 of 64 parks have grown and 10 have declined.** Absolute and relative change tell different stories, which I think is the most interesting result. 

The largest absolute gains went to parks that were already busy and the fastest relative growth went to small and remote parks, where a modest gain is enormous in percentage terms. American Samoa's figure is the least meaningful of these, since it is measured against a baseline of about 1,000 visits a year.

That was the most useful thing I learned from the data. Several parks have single-year jumps no real trend could produce.

# Development Environment

I developed this software in Visual Studio Code and used Git for version control, publishing the project to GitHub. I inspected results by writing them to CSV files and opening them, which let me check each stage before moving to the next.

The program is written in Python and uses pandas for all of the data handling and matplotlib for the charts. The project is split into four scripts: one to clean the raw data, one for each question, and one to produce the charts. Each writes its results to a CSV so the next stage can read them, which meant I could rerun one stage without redoing the others.

# Useful Websites

* [NPS Visitor Use Statistics](https://irma.nps.gov/Stats/)
* [Pandas Getting Started Tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html)
* [Matplotlib pyplot tutorial](https://matplotlib.org/stable/tutorials/pyplot.html)

# Future Work

* Set a minimum baseline before reporting a percentage, so a park growing from 1,000 visits does not top the growth chart
* Exclude park-years that record zero visits, which currently pass the twelve-month completeness check
* Bring in monthly weather data so "best month" can weigh conditions against crowds rather than crowds alone

# AI Disclosure

I used Claude as a learning and reference tool during this project. The help I received was in choosing the project, understanding the raw dataset, and reviewing my work against the data. It helped me understand the data and filtered it down to recreation visits for the 64 designated National Parks.

The largest single piece of help was understanding the raw file and creating new csv files to understand and filter the code better. The NPS export is in long format, and I did not know what the fifteen codes meant. The codes were decoded for me and the relationships between them were verified, which is how I knew to filter on TRV for recreation visits. I was also warned about two problems I would not have caught: the first file I downloaded splits each park's visits across the states it sits in, so Yellowstone appeared twice and summing by park alone would have reported less than half its real visitation; and the export contains all 400-plus NPS units rather than only the National Parks, which is why I built a separate lookup file of the 64 parks.

I also asked for a code review, and I was given both code-level and data-level feedback. 

I learned a lot about how to manipulate data and make it understandable. It doesn't exactly answer all of my questions, because it doesn't take the weather into account, but it still shows me the possibilities of what data analysis can do. 

Another thing I learned was the importance of defining the questions. Defining was "best" meant for my first question. I decided a strict comparisson to park visiotrs didn't really decide what "best" meant because of the weather. The 25% usability threshold is a decision I implemented so that the data didn't just say "January" every time because of the cold weather and lack of trips made. 