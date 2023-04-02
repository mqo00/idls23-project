import React, { useState } from 'react';
import RandQA from "./RandQA";
import AskQ from "./AskQ";
import HumanEvalA from "./HumanEvalA";
import './App.css';

// Model selection state variable
// Get/Post question & answer component
// Evlaute answer component: humanEval & machineEval display
function App() {

  const [state, setState] = useState({
    qa: {"key": "", "answer": ""},
    askq: false,
    reset: false, // a toggle rather than a flag, watch change
    model: "gpt-3.5-turbo zero-shot",
  });

  const newQA = (current_qa) => {
    setState(prevState => { return {...prevState, qa: current_qa} } );
  }
  const resetQA = () => { 
    setState(prevState => { return {...prevState, reset: !prevState.reset} } );
  }
  const flipAskq = () => {
    setState(prevState => { return {...prevState, askq: !prevState.askq} } );
  }

  // const setModel = (model) => { setState(prevState => { return {...prevState, model: model} } );}

  return (
    <div className="App">
      <div className='title'>
        <h1>Final Project Demo: AI TA for Piazza</h1>
      </div>
      <div className='model'>
        <h2>Model: {state.model} </h2>
      </div>
      <div className='qa-demo'>
      {/* <button className="button-19 green" onClick={() => setModel("gpt-3.5-turbo + prompt engineering")}>Prompt Exploration</button> */}
      <button className="button-19" onClick={flipAskq}>{state.askq ? "Get Random Example" : "Ask Your Own Question"}</button>
        {state.askq ? <AskQ newQA={newQA} reset={state.reset} /> : <RandQA newQA={newQA} reset={state.reset} />}
      </div>
      <div className='eval'>
        <HumanEvalA qaKey={state.qa.key} gpt_answer={state.qa.answer} resetQA={resetQA} />
      </div>
    </div>
  );
}

export default App;
