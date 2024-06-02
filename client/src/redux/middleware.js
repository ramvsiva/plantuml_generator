import axios from "axios";

const apiMiddleware = store => next => action => {
  if (!action.apiPackage) return next(action);

  const { type, apiPackage } = action;
  const { headers, body, method, parameters, query, responseType } = apiPackage;

  next({
    type: `${type}_PENDING`,
  });
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