import React from 'react';
import './App.css';
import { Row, Col} from 'antd';

import img1 from './images/0/00754.png';
import img2 from './images/1/00754.png';
import {ReactComponent as ReactLogo} from './images/ai.svg';

function App() {
  return (
    <div className="App">
     <p>什么是姿势评估</p> 

     <Row>
      <Col flex={3}>
        <p>原图</p>
        <div className="paper">
          <img width="300px" src={img1} />
        </div>
        {/* <div className="card"> */}
          {/* <img width="300px" src={img1} />
        </div>
        <div className="card">
          <img width="300px" src={img1} />
        </div> */} 
      </Col>
      <Col flex={3}>
        <ReactLogo style={{fill: "white", width: 300, height: 300, marginTop: 100}}/>
        <br />
        <svg height={40} style={{marginTop: 50}} transform="translate(20)">
        {/* <defs> 
          <marker id="arrow" markerWidth="10" markerHeight="10" orient="auto" markerUnits="strokeWidth"> 
          <path d="M0,0 L0,6 L9,3 z" fill="white" />  
          </marker>
        </defs>
        <line 
            x1="0" 
            y1="0" 
            x2="400" 
            y2="0" 
            style={{stroke:'white', strokeWidth:20}}
            marker-end="url(#arrow)"  
        /> */}
        <defs> <marker id="arrow" markerWidth="10" markerHeight="10"  orient="auto" markerUnits="strokeWidth" refX="0" refY="3"> <path d="M0,0 L0,4 L6,2 z" fill="#fff" /> </marker> </defs> 
        <line x1="0" y1="0" x2="240" y2="0" stroke="#ffff" stroke-width="10" marker-end="url(#arrow)" />
        </svg>
        <p style={{fontSize: "60%"}}> 神经网络 </p>
      </Col>
      <Col flex={3}>
        <p>骨架图(2D)</p>
        <div className="paper2">
        <img width="300px" src={img2} />
        </div>
      </Col>
    </Row>
    </div>
  );
}

export default App;
