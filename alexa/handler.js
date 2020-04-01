'use strict';
const AWS = require('aws-sdk');
const Alexa = require("alexa-sdk");
const lambda = new AWS.Lambda();
const dynamoDb = new AWS.DynamoDB.DocumentClient();
const uuid = require('uuid');

exports.handler = function(event, context, callback) {
  const alexa = Alexa.handler(event, context);
  alexa.appId = "amzn1.ask.skill.264ad7f0-dc68-4f68-8f3e-ae9441f492e0";
  alexa.registerHandlers(handlers);
  alexa.execute();
};

const handlers = {
  'LaunchRequest': function () {
    this.emit('Prompt');
  },
  'Unhandled': function () {
    this.emit('AMAZON.HelpIntent');
  },

  'LogMood': function () {
    var dayvalue = this.event.request.intent.slots.DayValue.value;
    var timestamp = new Date().getTime();
    var userId =  this.event.context.System.user.userId;

    console.log("recording data: ", dayvalue);

    const dynamodbParams = {
      TableName: process.env.DYNAMODB_TABLE_MOODS,
      Item: {
        id: uuid.v4(),
        userId: userId,
        dayvalue: dayvalue,
        createdAt: timestamp,
      },
    };

    dynamoDb.put(dynamodbParams).promise()
    .then(data => {
      this.emit('AMAZON.StopIntent');
    })
    .catch(err => {
      console.error(err);
      this.emit(':tell', 'I had a problem saving your data.');
    });


  },
  'AMAZON.YesIntent': function () {
    this.emit('Prompt');
  },
  'AMAZON.NoIntent': function () {
    this.emit('AMAZON.StopIntent');
  },
  'Prompt': function () {
    this.emit(':ask', 'Please tell me how your day was', 'Please tell me again?');
  },
  'NoMatch': function () {
    this.emit(':ask', 'Sorry, I couldn\'t understand.', 'Please say that again?');
  },
  'AMAZON.HelpIntent': function () {
    const speechOutput = 'You need to mention expense amount and a category';
    const reprompt = 'Say hello, to hear me speak.';

    this.response.speak(speechOutput).listen(reprompt);
    this.emit(':responseReady');
  },
  'AMAZON.CancelIntent': function () {
    this.response.speak('Goodbye!');
    this.emit(':responseReady');
  },
  'AMAZON.StopIntent': function () {
    this.response.speak('Thank you for sharing your day with me. See you tomorrow!');
    this.emit(':responseReady');
  }
};
