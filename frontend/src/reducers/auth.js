import {
    LOGIN_FAIL,
    LOGIN_SUCCESS,
    USER_LOAD_FAIL,
    USER_LOAD_SUCCESS
} from "../actions/types";

const initialState = {
    access: localStorage.getItem('access'),
    refresh: localStorage.getItem('refresh'),
    user: null,
    isAuthenticated: null,
};

export default function (
    state = initialState, action
)
{
   const {type, payload } = action;

   switch(type) {
       case LOGIN_SUCCESS:
           localStorage.setItem('access', payload.access);

           return {
                ...state,
               isAuthenticated: true,
               access: payload.access,
               refresh: payload.refresh,
           }
       case USER_LOAD_SUCCESS:

           return {
               ...state,
               user: payload
           }

       case USER_LOAD_FAIL:
           return {
                ...state,
               user: null
           }
       case LOGIN_FAIL:
           localStorage.removeItem('refresh');
           localStorage.removeItem('access');
           return {
                ...state,
               isAuthenticated: false,
               access: null,
               refresh: null,
               user: null,
           }
       default:
           return state;
   }
}