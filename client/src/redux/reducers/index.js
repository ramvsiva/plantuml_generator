import { combineReducers } from 'redux';

import umlReducer from "./umlReducer";

const plantUmlReducer = combineReducers({
    umlReducer,

  });

export default plantUmlReducer;