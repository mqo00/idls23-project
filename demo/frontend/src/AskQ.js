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
    }, [reset]);

    const handleChange = (event) => {
        setQuestion(event.target.value);
    }

    const handleSubmit = async (event) => {
        setAnswer("Loading ...");
        newQA({"key": "", "answer": ""});
        event.preventDefault();
        // const { data } = await axios.post(`${process.env.REACT_APP_API_URL}/submit_question`, { question });
        const { answer, hash } = await postq_geta(question);
        setAnswer(answer);
        newQA({"key": hash, "answer": answer});
    }

    // an input text box & button for submit question rows="5" cols="50"
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