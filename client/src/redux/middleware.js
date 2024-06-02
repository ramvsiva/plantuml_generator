import axios from "axios";

/**
 * Redux middleware for handling API requests as part of dispatched actions.
 * This middleware checks for an 'apiPackage' in the action to determine if it should
 * process an API request. If 'apiPackage' is present, it will execute the request and
 * dispatch subsequent actions based on the request's outcome.
 *
 * @param {Object} store - The Redux store.
 * @returns {Function} - Returns a function that handles the next middleware in the chain.
 */

const apiMiddleware = store => next => action => {
  // Check if the action should be processed by this middleware
  if (!action.apiPackage) return next(action);

  // Extract details necessary for making the API call from the action
  const { type, apiPackage } = action;
  const { headers, body, method, parameters, query, responseType } = apiPackage;

  // Notify that the API request is starting
  next({
    type: `${type}_PENDING`,
  });

  // Perform the API request using axios
  axios({
    method: method,
    url: parameters,
    data: body || null,
    params: query,
    responseType: responseType || null,
    headers: { 'X-API-Key': "VGT-LOI-8713", ...headers },
  })
    .then(res => {
      const { apiPackage, ...restAction } = action;
      console.log(res.data)
      store.dispatch({
        ...restAction,
        type: `${type}_SUCCESS`,
        response: res.data
        
      });
    })
    .catch((error) => {
      console.log('err: ', error)
      store.dispatch({
        type: `${type}_FAILURE`
      });
    });
};

export default apiMiddleware;
