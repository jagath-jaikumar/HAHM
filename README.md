# 692M Project Proposal
### HAHM: Home Assistant Health Monitor
### Jagath Jai Kumar

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/Naereen/)

[![ForTheBadge makes-people-smile](http://ForTheBadge.com/images/badges/makes-people-smile.svg)](http://ForTheBadge.com)

[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)




# Problem

Many of my friends seek therapy and/or check in regularly with a physician to monitor health and mental issues. They often struggle to keep a daily log of their pain and progress, and have a hard time remembering specific details when talking to doctors. This causes them to have problems scheduling meetings and appointments at pertinent times.


# Solution

My proposal for addressing this problem is HAHM (Home Assistant Health Monitor) - A home assistant app that checks in with the user daily to gauge mood, pain, and quality of the user’s day. The user would be able to come home and talk to HAHM via Amazon Alexa or Google Home and tell the device about how the user is feeling.
HAHM would then record the User’s response, counting the instances of positive and negative words to recognize and record the type of day for the user. Over several weeks, HAHM will keep a log of the user’s mood, and the user can check in with the HAHM mobile app to see how they have been feeling or remember specific dates. Therapists and doctors can have up-to-date records of their patients mood, and will be able to ask specific questions to patients when having face-to-face interactions.


# Existing Technology

There are several existing apps on the app store that deal with physical health and lifestyle monitoring, however none have vocal home assistant integration. There are no equivalent Alexa skills that are available which are built to have daily mood conversations with the user. The most similar app currently available on the iOS app store is Symple Symptom Tracker, which allows users to manually enter in data about their mood and daily symptoms. Some sensor based health recording apps are available, but they require the user to wear sensors throughout the day. HAHM will use home assistant technology to remind the user and make daily logging part of the user’s routine while being more ubiquitous and less intrusive.


# Technologies

- Amazon Alexa and Alexa Skills Kit, Python
- Ionic
- Plotly Dash, Python
- AWS S3 and Lambda, Python
The mobile companion would be a very basic app just showing the general mood of the user over time, and the Therapist Web portal would allow mental health professionals to monitor several patients at once.

# Proposed Milestones
- Build Amazon Alexa skill with number mood ranking (1-10 based on quality of day)
- Save response to cloud DB (AWS S3)
- Build iOS app to read from DB and display daily log to user
- Build Web companion App for health professionals to monitor multiple users

# Extended Milestones
- Upgrade Alexa skill to include NLP for phrase responses
- Upgrade Alexa skill to include support for pain/trauma response (1-10 user pain during health recovery)
- Build Android companion app
