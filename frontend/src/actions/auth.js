import {
    LOGIN_FAIL,
    LOGIN_SUCCESS,
    USER_LOAD_FAIL,
    USER_LOAD_SUCCESS
} from "./types";

import axios from "axios";

export const load_user = () => async dispatch => {
};

export const login = (email, password) => async dispatch => {
    const config = {
        header: {
            'Content-Type': 'application/json',
        }
    };

    const body = JSON.stringify({email, password});

    try {
        const res = await axios.post(`${process.env["REACT_APP_API_URL"]}/login/auth/`, body, config)
        console.log(res);
        dispatch({
            type: LOGIN_SUCCESS,
            payload: res.data,
        })
    }
    catch (err){
        console.log('123')
        dispatch({
            type: LOGIN_FAIL
        })
    }
};