import React from 'react';
import { render } from 'react-dom';
import App from './App';
import store from './redux/store';
import { Provider } from "react-redux";

const local = navigator.language;

render(
  <React.StrictMode>
    <Provider store={store}>
        <App />
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);