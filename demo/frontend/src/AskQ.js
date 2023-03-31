// class component AskQ
import React, { useEffect, useState } from 'react';
import { postq_geta } from './requests';

// submit question to get model answer
function AskQ ({newQA, reset}) {
    
    const [question, setQuestion] = useState("IDL Piazza Question @");
    const [answer, setAnswer] = useState("");

    useEffect (() => {
        newQA({"key": "", "answer": ""});
        setQuestion("IDL Piazza Question @");
        setAnswer("");
    // eslint-disable-next-line
    }, [reset]);

    const handleChange = (event) => {
        setQuestion(event.target.value);
    }

    const handleSubmit = async (event) => {
        setAnswer("Loading ...");
        newQA({"key": "", "answer": ""});
        event.preventDefault();
        const { answer, hash } = await postq_geta(question);
        setAnswer(answer);
        newQA({"key": hash, "answer": answer});
    }

    return (
        <div className="qa-block">
            <div className="qa">
            <div className="question">
                <h2>Ask Your Own Question</h2>
                <form onSubmit={handleSubmit}>
                    <div className='user-input white'>
                    <textarea onChange={handleChange} value={question}
                        placeholder="Enter/Paste your question here."
                    ></textarea>
                    </div>
                    <input className="submit-btn" type="submit" value="Ask the model" />
                </form>
            </div>
            </div>
            <div className="gpt-answer">
                <h2>Model Answer</h2>
                <div className="multiline-p">{answer}</div>
            </div>
        </div>
        );
    }

export default AskQ;