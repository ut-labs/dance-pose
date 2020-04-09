import React from 'react';
import './App.css';
import { Row, Col} from 'antd';
import {Deck, Slide, Heading, Box } from 'spectacle';
import defaultTheme from './theme/default-theme';

import img1 from './images/0/00754.png';
import img2 from './images/1/00754.png';
import {ReactComponent as ReactLogo} from './images/ai.svg';

function App() {
  return (
    <div className="App">
      <Deck theme={defaultTheme}>
        <Slide>
          <Heading>
            什么是姿势评估？
          </Heading>
          <Box>
            <img src={img1} width="20%"/>
          </Box>
          <Box>
            <img src={img2} width="20%"/>
          </Box>
        </Slide>
      </Deck>
    </div>
  );
}

export default App;
