
import Select from 'react-select';

// import { colourOptions } from '../data';

import '../App.css';

import 'react-pro-sidebar/dist/css/styles.css';

import SidebarLayout from '../newcomponents/SidebarLayout';
import { useContext, useState } from 'react';
import DataExportTools from '../newcomponents/DataExportTools';
import Graph from '../newcomponents/Graph';
import { GlobalContext } from '../contexts/GlobalContext';
import DownloadGraphOptions from '../newcomponents/DownloadGraphOptions';
import { AuthPrompt } from '../newcomponents/AuthPrompt';

const MainGraph = () => {
    const { showGraph } = useContext(GlobalContext);
    return (
        <>
            <SidebarLayout width={290}>
                <AuthPrompt />
                <Graph />
            </SidebarLayout>
        </>
    )
}

export default MainGraph
