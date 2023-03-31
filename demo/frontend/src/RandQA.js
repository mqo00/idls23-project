// class component RandQA
// get random sample button: q, ta, gpt from backend
import React, { useEffect, useState } from 'react';
import { get_qa } from './requests';

function RandQA ({newQA, reset}) {

    const [qa, setQA] = useState({
        question: "Loading ...",
        ta_answer: "",
        gpt_answer: "",
        hash: "",
    });

    const getRandomQA = async () => {
        const { question, ta_answer, gpt_answer, hash } = await get_qa();
        setQA({question, ta_answer, gpt_answer, hash});
        newQA({"key": hash, "answer": gpt_answer});
    }
    
    // eslint-disable-next-line
    useEffect (() => {getRandomQA()}, [reset]);
    
    // display the question and both answers side by side
    return (
    <div className="qa-block">
        <div className="qa">
            <div className="question">
                <h2>Question</h2>
                <div className="multiline-p">{qa.question}</div>
            </div>
            <div className="ta-answer">
                <h2>TA Answer</h2>
                <div className="multiline-p">{qa.ta_answer}</div>
            </div>
        </div>
        <div className="gpt-answer">
            <h2>Model Answer</h2>
            <div className="multiline-p">{qa.gpt_answer}</div>
        </div>
    </div>
    );
}

export default RandQA;
