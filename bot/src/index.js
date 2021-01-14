const axios = require('axios').default;

module.exports = (app) => {
  app.log.info("[INFO] Labelling-Bot is up and running");

  app.on(["issues.opened", "pull_request.opened"], async (context) => {
    const {title, body} = context.payload.issue;

    let issueComment = "";
    axios.post("https://label-predictor.herokuapp.com/api/prediction", {title, body})
      .then((response) => response.data.predictedLabel)
      .then((predictedLabel) => {
        issueComment = context.issue({
          body: `Issue-Label Bot is automatically applying the label \`${predictedLabel}\` to this issue, with a confidence of 0.81.\nPlease mark this comment with 👍 or 👎 to give our bot feedback!\n\nLinks: [dashboard]() and [code](https://github.com/totsteps/labelling-bot) for this bot.`
        })

        return context.octokit.issues.createComment(issueComment);
      })
      .catch((error) => {
        app.log.error(error)
      })
  });


  app.on(["issues.opened", "pull_request.opened"], async (context) => {
    const {title, body} = context.payload.issue;

    axios.post("https://label-predictor.herokuapp.com/api/prediction", {title, body})
      .then((response) => response.data.predictedLabel)
      .then((predictedLabel) => {
        const labels = [predictedLabel];
        app.log.info(context.issue({labels}));
        return context.octokit.issues.addLabels(context.issue({labels}));
      })
      .catch((error) => {
        app.log.error(error)
      })
  });
};
