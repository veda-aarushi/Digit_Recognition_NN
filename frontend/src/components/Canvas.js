import React, { useRef, useEffect, useState } from "react";

const Canvas = ({ onSubmit }) => {
    const canvasRef = useRef(null);
    const [isDrawing, setIsDrawing] = useState(false);
    const [lastPos, setLastPos] = useState({ x: 0, y: 0 });

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.lineWidth = 16;
        ctx.lineCap = "round";
        ctx.strokeStyle = "black";
    }, []);

    const getMousePos = (e) => {
        const canvas = canvasRef.current;
        const rect = canvas.getBoundingClientRect();
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top,
        };
    };

    const handleMouseDown = (e) => {
        setIsDrawing(true);
        setLastPos(getMousePos(e));
    };

    const handleMouseMove = (e) => {
        if (!isDrawing) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        const currentPos = getMousePos(e);

        ctx.beginPath();
        ctx.moveTo(lastPos.x, lastPos.y);
        ctx.lineTo(currentPos.x, currentPos.y);
        ctx.stroke();

        setLastPos(currentPos);
    };

    const handleMouseUp = () => {
        setIsDrawing(false);
    };

    const clearCanvas = () => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    };

    const handleSubmit = () => {
        const canvas = canvasRef.current;
        canvas.toBlob((blob) => {
            const formData = new FormData();
            formData.append("file", blob, "digit.png");

            fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                body: formData,
            })
                .then((res) => res.json())
                .then((data) => onSubmit(data.prediction))
                .catch((err) => console.error("Prediction error:", err));
        }, "image/png");
    };

    return (
        <div>
            <canvas
                ref={canvasRef}
                width={280}
                height={280}
                style={{ border: "2px solid black", cursor: "crosshair" }}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
            />
            <div style={{ marginTop: "10px" }}>
                <button onClick={handleSubmit}>Predict</button>
                <button onClick={clearCanvas} style={{ marginLeft: "10px" }}>
                    Clear
                </button>
            </div>
        </div>
    );
};

export default Canvas;
