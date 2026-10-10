import React from 'react';
import {createRoot} from 'react-dom/client';
import ArtifactApp from './ArtifactApp';
import './styles.css';
createRoot(document.getElementById('root')!).render(<React.StrictMode><ArtifactApp/></React.StrictMode>);
