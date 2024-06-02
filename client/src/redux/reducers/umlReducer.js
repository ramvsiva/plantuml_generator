import {

    UML_GENERATION_PENDING,
    UML_GENERATION_SUCCESS,
    UML_GENERATION_FAILURE

} from '../constants/umlConstants';

/**
 * Defines the initial state of the UML generation data within the Redux store.
 */

const initialState = {
      umlGenerationState: {
    pending: false,
    success: false,
    failure: false
  },

    umlData: null
};

/**
 * Reducer for handling UML generation actions.
 * @param {Object} state - The current state of the UML generation.
 * @param {Object} action - Action dispatched to the reducer.
 * @returns {Object} - Updated state based on the action type.
 */

const umlReducer = (state = initialState, action) => {
      switch (action.type) {
    case UML_GENERATION_PENDING:
      return { ...state, umlGenerationState: { pending: true, success: false, failure: false } };
    case UML_GENERATION_SUCCESS:
      return { ...state, umlData: action.response, umlGenerationState: { pending: false, success: true, failure: false } };
    case UML_GENERATION_FAILURE:
      return { ...state, umlGenerationState: { pending: false, success: false, failure: true } };

    default:
      return state;
  }
}

export default umlReducer;

