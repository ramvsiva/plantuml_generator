import React, { useEffect, useState } from 'react';
import { connect } from 'react-redux';
import actions from './redux/actions/umlActions';

const App = ({ umlGenerationState, umlData, generateUml }) => {
  const [description, setDescription] = useState('');
  const [umlImage, setUmlImage] = useState();
  const [umlText, setUmlText] = useState();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (umlGenerationState?.pending) {
      setLoading(true);
    }
    if (umlGenerationState?.success && umlData) {
      setLoading(false);
      try {
        const contentType = 'image/jpeg';
        const blob = b64toBlob(umlData.payload, contentType);
        const blobUrl = URL.createObjectURL(blob);
        setUmlImage(blobUrl);
        setUmlText(null);
      } catch (e) {
        setUmlText(umlData.payload);
        setUmlImage(null);
      }
    }
  }, [umlGenerationState]);

  const b64toBlob = (b64Data, contentType, sliceSize = 512) => {
    const byteCharacters = atob(b64Data);
    const byteArrays = [];
    for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
      const slice = byteCharacters.slice(offset, offset + sliceSize);
      const byteNumbers = new Array(slice.length);
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      byteArrays.push(byteArray);
    }
    return new Blob(byteArrays, { type: contentType });
  };

  const handleSubmit = () => {
    generateUml(description);
  };

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <input
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        style={{ margin: '20px', padding: '10px', width: '300px', borderRadius: '5px', border: '2px solid #ccc' }}
        placeholder="Enter PlantUML Prompt"
      />
      <button onClick={handleSubmit} style={{ padding: '10px 20px', borderRadius: '5px', backgroundColor: '#4CAF50', color: 'white', border: 'none', cursor: 'pointer' }}>
        Generate UML
      </button>
      {loading ? (
        <div style={{ margin: '20px' }}>
          <div className="spinner" style={{ width: '50px', height: '50px', border: '5px solid #f3f3f3', borderTop: '5px solid #3498db', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
        </div>
      ) : (
        <div style={{ marginTop: '20px' }}>
          {umlImage ? (
            <img src={umlImage} alt="Generated UML" style={{ maxWidth: '100%', maxHeight: '400px' }} />
          ) : (
            <textarea readOnly value={umlText || "Enter a description and generate UML."} style={{ width: '300px', height: '200px', padding: '10px', borderRadius: '5px', border: '2px solid #ccc' }} />
          )}
        </div>
      )}
    </div>
  );
};

const mapStateToProps = state => ({
  umlGenerationState: state.umlGenerationState,
  umlData: state.umlData
});

const mapDispatchToProps = dispatch => ({
  generateUml: (description) => dispatch(actions.generateUml(description)),
});

export default connect(mapStateToProps, mapDispatchToProps)(App);
