// class component HumanEvalA

import React, { useEffect, useState } from 'react';
import { post_feedback } from './requests'; 
import { ToggleButton, ToggleButtonGroup } from '@mui/material';
import { SentimentNeutral, SentimentVerySatisfied, SentimentVeryDissatisfied } from '@mui/icons-material';

function HumanEvalA ({qaKey, gpt_answer, resetQA}) {
    
    const placeholder = "Edit to improve the answer.";
    
    const [humanEval, setHumanEval] = useState({
        label: "",
        improve: gpt_answer,
    });

    // eslint-disable-next-line
    useEffect (() => {setHumanEval({...humanEval, label: "", improve: gpt_answer})}, [gpt_answer]);
    
    const handleChange = (event) => {
        const { name, value } = event.target;
        setHumanEval(prevState => { return {...prevState, [name]: value} } );
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        const { label, improve } = humanEval;
        const update_dict = {"label": label, "edit": improve }
        await post_feedback(qaKey, update_dict);
        setHumanEval({...humanEval, label: "", improve: placeholder});
        resetQA();
    }

    // label: Incorrect, Unhelpful, Great with three different buttons, submit to backend
    // also enable edit for gpt-answer, how would you change the generation
    return (
        <div className="human-eval">
            <h2>Evaluate & Edit model's answer to improve it</h2>
            <form className="eval-form" onSubmit={handleSubmit}>
                <ToggleButtonGroup className='label-btn' orientation="vertical"
                value={humanEval.label} exclusive onChange={handleChange}>
                    <ToggleButton name="label" color="error" value="incorrect" aria-label="incorrect">
                        <SentimentVeryDissatisfied />Incorrect</ToggleButton>
                    <ToggleButton name="label" color="warning" value="unhelpful" aria-label="unhelpful">
                        <SentimentNeutral />Unhelpful</ToggleButton>
                    <ToggleButton name="label" color="success" value="great" aria-label="great">
                        <SentimentVerySatisfied />Great</ToggleButton>
                    <input className="submit-btn" type="submit" value="Subimt Feedback" />
                </ToggleButtonGroup>
                <div className="user-input">
                    <textarea name="improve" onChange={handleChange} value={humanEval.improve}
                    placeholder={placeholder}></textarea>
                </div>
            </form>
        </div>
    );
}

export default HumanEvalA;