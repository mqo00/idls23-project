import axios from 'axios';

// get_qa: get random question and answer from backend
async function get_qa() {
    try {
        const { data } = await axios.get(`${process.env.REACT_APP_API_URL}/get_random_qa`);
        // console.log(data);
        return data;
    } catch (error) {
        console.log(error);
    }
}

// postq_geta: post question to backend and get answer
async function postq_geta(question) {
    try {
        const { data } = await axios.post(
            `${process.env.REACT_APP_API_URL}/submit_question`, { question }
        );
        // console.log(data);
        return data;
    } catch (error) {
        console.log(error);
    }
}

// post_prompt_q: post prompt to backend and get answer & full prompt (messages)
async function post_prompt_q(question, num_rand_ex, fix_prompt) {
    try {
        const { data } = await axios.post(
            `${process.env.REACT_APP_API_URL}/submit_prompt_question`, { question, num_rand_ex, fix_prompt }
        );
        // console.log(data);
        return data; // messages, answer
    } catch (error) {
        console.log(error);
    }
}

// post_feedback: post human evaluation to backend
async function post_feedback(key, update_dict) {
    try {
        const { data } = await axios.post(
            `${process.env.REACT_APP_API_URL}/submit_feedback`, { key, update_dict }
        );
        // console.log("post_feedback:", data);
        return data;
    }
    catch (error) {
        console.log(error);
    }
}

export {get_qa, postq_geta, post_feedback, post_prompt_q};