import React, { Component } from 'react';
import axios from 'axios';
import './App.css';

// App component
// Model selection state variable
// Get/Post question & answer component
//  get sample button: q, ta, gpt
//  submit question text box & button
// Evlaute answer component: label true/false/edit 

class App extends Component {
  state = {
    questions: ["Loading..."],
    question: "",
    ta_answer: "",
    gpt_answer: "",
  }

  componentDidMount() {
    this.fetchQuestions()
  }

  fetchQuestions = async () => {
    const { data } = await axios.get(
      `${process.env.REACT_APP_API_URL}/get_random_qa`,
    );
    const { questions } = data;
    this.setState({questions})
  }

  handleChange = (event) => {
    this.setState({question: event.target.value});
  }

  handleSubmit = (event) => {
    this.fetchAnswer();
    event.preventDefault();
  }

  fetchAnswer = async () => {
    const { question } = this.state;
    const { data } = await axios.post(
      `${process.env.REACT_APP_API_URL}/submit_question`, { question }
    );
    const { answer } = data;
    this.setState({answer})
  }

  render() {
    const { questions, question, answer } = this.state;
    return (
      <div className="App">
        <header className="App-header">
        <h1>List of questions</h1>
        <ul>
          {questions.map(question => (<li key={question}>{question}</li>))}
        </ul>
          <form onSubmit={this.handleSubmit}>
          <label>
            Question:
            <input type="text" value={question} onChange={this.handleChange} />
          </label>
          <input type="submit" value="Submit" />
        </form>
        <h1>Answer: {answer}</h1>
        </header>
      </div>
    );
  }
}

export default App;
