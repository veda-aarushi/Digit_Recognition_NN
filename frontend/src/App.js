import React, { useState } from "react";
import Canvas from "./components/Canvas";

function App() {
    const [prediction, setPrediction] = useState(null);

    return (
        <div style={{ textAlign: "center", marginTop: "40px" }}>
            <h1>🧠 Handwritten Digit Recognizer</h1>
            <Canvas onSubmit={setPrediction} />
            {prediction !== null && (
                <h2 style={{ marginTop: "20px" }}>Prediction: {prediction}</h2>
            )}
        </div>
    );
}

export default App;
