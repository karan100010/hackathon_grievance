const mongoose = require("mongoose");

const commentSchema = new mongoose.Schema(
  {
    text: { type: String },
    userId: { type: mongoose.Schema.Types.ObjectID },
  },
  { timestamps: true }
);

const Comment = mongoose.model("Comment", commentSchema);

module.exports = Comment;
