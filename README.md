# ETF RoboAdvisor: AWS Lex & Lambda
### Project #2, UNCC/Trilogy Education Services *FinTech Bootcamp*

According to a 2016 [poll](https://www.businessinsider.com/chatbots-vs-humans-for-customer-relations-2016-12), 44% of 18 - 65 year old users preferred interacting with chatbots over humans for standard customer relationship management (CRM) situations. As young adults continue to acquire customer market share, it is presumed this number has risen steadily since. Of course, market share gains come alongside income growth, which tends to be when people start to think about growing their wealth.

Studies abound of Gen Z's (and certain Milleanials') aversion to human interaction when it comes to routine tasks as compared with older generations. Discussing financial matters with an advisor can be daunting to anyone, but the market's fastest-growing consumer section expresses this quite clearly. A prime example is the average age of a Robinhood account owner, which is significantly lower than that of the average advisor-managed account holder. 

Given these facts, we have developed a chatbot to recommend ETF holdings to interested investors, which will likely be Gen Zers and Millenials. ETFs have the benefit of mitigating the risk that comes with selecting a handful of individual stocks when on a limited budget (again, a young investor trait. Specifically, our bot recommends SPDR industry ETFs, as they are widely reported on and easier to grasp for new investors. Our bot inquires as to the user's investment period, risk appetite, and return goals, among other things.

---

## Technologies

In order to utilize our project, you will need an Amazon Web Services (AWS) account to access the various technologies leveraged. Our project was created using their free options, so you can run it with a free user account as well. All work was done under one root account, with each team member having their own administrator (IAM) account nested within it.

Amazon Web Services used:

- Amazon Simple Storage Service (S3)
- Amazon Lex
- Amazon DynamoDB
- AWS Lambda

All Lambda code was completed in the **Python 3.7** runtime. 

Ensure through your local terminal that your development environment supports the following imports and dependencies. If it does not, reference your terminal installation guide to download the missing software:

* EllieBackStage_GT Lambda function import requirements:
```
from datetime import datetime
from dateutil.relativedelta import relativedelta
from botocore.vendored import requests
```

* Ellie_Sector_Selector Lambda function import requirements:
```
from datetime import datetime
from dateutil.relativedelta import relativedelta
from botocore.vendored import requests

# Required libraries to connect to S3 bucket and read JSON files
import boto3
import json
import uuid
```

* Financial analysis .ipynb file import requirements:
 ```
import investpy.etfs as etfs
import pandas as pd
import numpy as np
import hvplot.pandas as hvplot

# Note that plots were used on the backend only to assist in selecting relevant information for the Ellie Lex bot to return to the user.
 ```
The financial analysis which this project utilizes comes from the *investpy* Python library. It is a webscraping library that gets its information from the popular site Investing.com.


---

## Usage

Stepping through our Ellie chatbot is a simple process: initiate the conversation, provide the relevant information pertaining to your risk appetite, investment amount, etc. when prompted, and decide on a SPDR ETF that is to your liking. Below is an example of the conversation flow to expect when interacting with Ellie:

![Conversation Flow pt. 1](./ellie_convo_1.png)

![Conversation Flow pt. 2](./ellie_convo_2.png)

![Conversation Flow pt. 3](./ellie_convo_3.png)

![Conversation Flow pt. 4](./ellie_convo_4.png)

---

## Contributors

E. Kenny

- [LinkedIn](https://www.linkedin.com/in/e-kenny/)

- [Email](ekenny3@uncc.edu)

B. Miller

- [LinkedIn](https://www.linkedin.com/in/brian-miller-ft421/)

- [Email](bam4217@yahoo.com)

G. Taraboletti

- [LinkedIn](https://www.linkedin.com/in/giselle-taraboletti/)

- [Email](gtaraboletti@gmail.com)

---

## License

MIT

License file included in repository.
