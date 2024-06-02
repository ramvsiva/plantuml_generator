import {
  UML_GENERATION
} from '../constants/umlConstants';

const baseUrl = process.env.REACT_APP_SERVER_BASE_URL;

/**
 * Action creator for generating UML diagrams.
 * @param {string} description - The description based on which the UML is generated.
 * @returns {Object} - Redux action to trigger UML generation.
 */

const generateUml = (description) => ({
  type: UML_GENERATION,
  apiPackage: {
    method: 'POST',
    parameters: `${baseUrl}/uml/generator/`,
    body: { description: description }
  }
});

// Collection of all action creators related to UML generation.
const actions = {
  generateUml
}

export default actions;
