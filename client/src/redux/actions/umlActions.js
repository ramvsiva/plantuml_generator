import {
  UML_GENERATION
} from '../constants/umlConstants';

const baseUrl = process.env.REACT_APP_SERVER_BASE_URL

const generateUml = (description) => ({
  type: UML_GENERATION,
  apiPackage: {
    method: 'POST',
    parameters: `http://52.57.216.207:8070/uml/generator/`,
    // parameters: `${baseUrl}/uml/generator/`,
    body: { description: description }
  }
});

const actions = {
  generateUml
}

export default actions;