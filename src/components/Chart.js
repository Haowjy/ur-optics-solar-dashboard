import {
    LineChart, Line,
    CartesianGrid, XAxis, YAxis, Tooltip,
    Label, Legend
} from 'recharts';

import { Resizable } from 'react-resizable';

import React, { useState, useContext } from 'react'

import arrowdown from '../images/drop-down-arrow.svg';
import arrowup from '../images/up-arrow.svg';
import copyicon from '../images/copy.svg';

import '../App.css';
import "./react-resizable.css";

//todo change to only import individual components
import { Button, Form, Collapse, Row, Col, OverlayTrigger, Tooltip as BSTooltip } from 'react-bootstrap';

import { defaultGraphOptions, graphColors } from '../DefaultConstants';
import { DataFormContext } from '../contexts/DataFormContext';
import { useDownloadChartSubmit } from '../hooks/useDownloadChartSubmit';

/** @typedef StateSetter */
/**
 * Chart functional component to display data selected from DataSelection
 * @param  {{graphData:, graphLines: Array.<string>, irridianceGraphLines: Array.<string>, meteorologicalGraphLines: Array.<string>, copyLinkText: string, setCopyLinkText: StateSetter, createQuery: function}} props
 */
const Chart = ({ graphData, graphLines,
    irridianceGraphLines, meteorologicalGraphLines,
    createQuery, copyLinkText, setCopyLinkText }) => {

    const { graphTitle, scrollRef } = useContext(DataFormContext);

    const [copiedState, setCopiedState] = useState(false);
    const [graphOptions, setGraphOptions] = useState(JSON.parse(localStorage.getItem("graphOptions")) || defaultGraphOptions);
    const [downloadSelection, setDownloadSelection] = useState(0);
    const [handleChartSubmit] = useDownloadChartSubmit({ downloadSelection, graphData });

    const [size, setSize] = useState({ width: 1000, height: 600 });

    /**
     * 
     * @param {*} event 
     * @param {{element, size}} param1 
     */
    const onResize = (event, { element, size }) => {
        setSize({ width: size.width, height: size.height });
    }

    return (
        <div ref={scrollRef}>
            <h2>Graph
                <OverlayTrigger
                    placement="bottom-start"
                    delay={{ show: 50, hide: 100 }}
                    overlay={<BSTooltip id="button-tooltip">{copiedState ? "Copied!" : copyLinkText}</BSTooltip>}
                    onToggle={(show) => {
                        if (!show) {
                            console.log("onHide");
                            setCopyLinkText(createQuery());
                            setCopiedState(false);
                        } else {
                            console.log("onshow");
                        }
                    }}
                >
                    <img alt="copy icon" src={copyicon} style={{ marginLeft: "10px", cursor: "pointer" }} width={20} height={20}
                        onClick={() => {
                            navigator.clipboard.writeText(copyLinkText)
                                .then(() => {
                                    setCopiedState(true);
                                })
                                .catch(err => {
                                    console.log('Something went wrong', err);
                                });
                        }}
                    />
                </OverlayTrigger>
            </h2>
            <div style={{ marginLeft: "24px" }}>
                <h4
                    style={{ opacity: "0.75", cursor: "pointer" }}
                    onClick={() => setGraphOptions({ ...graphOptions, 'show-graph-options': !graphOptions['show-graph-options'] })}>
                    Graph Options
                    <img src={graphOptions["show-graph-options"] ? arrowup : arrowdown} alt={graphOptions["show-graph-options"] ? "arrow up" : "arrow down"} style={{ marginLeft: "10px" }} width={10} height={10} />
                </h4>
                <Collapse in={graphOptions["show-graph-options"]}>
                    <div>
                        <Form>
                            <Row>
                                <Col sm="2">
                                    <Button variant="outline-primary" onClick={() => setGraphOptions({ ...defaultGraphOptions, "show-graph-options": graphOptions["show-graph-options"] })}>
                                        Reset
                                    </Button>
                                </Col>
                            </Row>

                            <Form.Group as={Row}>
                                <Col sm="2">
                                    <Form.Label style={{ marginTop: "5px" }}>
                                        Line Thickness: {graphOptions["line-thickness"]}
                                    </Form.Label>
                                </Col>
                                <Col sm="4">
                                    <Form.Control type="range" min={1} max={5} step={0.5} style={{ marginTop: "10px" }}
                                        value={graphOptions["line-thickness"]}
                                        onChange={e => setGraphOptions({ ...graphOptions, "line-thickness": e.target.value })}
                                    />
                                </Col>
                            </Form.Group>

                            <Form.Group as={Row}>
                                <Col sm="2">
                                    <Form.Label style={{ marginTop: "5px" }}>
                                        Font Size: {graphOptions["font-size"]}
                                    </Form.Label>
                                </Col>
                                <Col sm="4">
                                    <Form.Control type="range" min={12} max={28} step={1} style={{ marginTop: "10px" }}
                                        value={graphOptions["font-size"]}
                                        onChange={e => setGraphOptions({ ...graphOptions, "font-size": e.target.value })}
                                    />
                                </Col>
                            </Form.Group>

                            <Form.Check
                                type={'checkbox'}
                                id={'legend'}
                                name={'legend'}
                                checked={graphOptions["legend"]}
                                label={'Legend'}
                                onChange={(event) => setGraphOptions({ ...graphOptions, [event.target.name]: event.target.checked })} />

                        </Form>
                    </div>
                </Collapse>
            </div>

            <div className="layoutRoot">
                <Resizable
                    className="box"
                    minConstraints={[800, 600]}
                    height={size.height}
                    width={size.width}
                    onResize={onResize}
                >
                    <div
                        className="box"
                        style={{
                            width: size.width + "px",
                            height: size.height + "px"
                        }}
                    >
                        <div id="lineChart">
                            <h3 style={{ paddingTop: 12 }}>{graphTitle}</h3>
                            <>
                                <LineChart
                                    data={graphData}
                                    margin={{ top: 24, right: 128, left: 64, bottom: 108 }}
                                    width={size.width} height={size.height}
                                >
                                    <defs>
                                        <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                                            <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                                        </linearGradient>
                                        <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8} />
                                            <stop offset="95%" stopColor="#82ca9d" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    {/* TODO: Xaxis formatter, based on day, month, etc */}
                                    <XAxis dataKey="datetime" xAxisId={0} tickCount={1} minTickGap={359} interval={graphOptions["font-size"] > 24 ? 359 : 179}
                                        style={{ fontSize: graphOptions["font-size"] }}
                                        height={36} />

                                    <XAxis dataKey="date" xAxisId={1} tickCount={1} interval={1439}
                                        style={{ fontSize: graphOptions["font-size"] }} >
                                        <Label dy={20} value="America/New_York" offset={0} position="insideBottom" style={{ fontSize: graphOptions["font-size"] }} />
                                    </XAxis>


                                    {(irridianceGraphLines.length === 0) ? null :
                                        <YAxis yAxisId="left" label={<Label
                                            value="Irridiance"
                                            position="insideLeft"
                                            angle={-90}
                                            style={{ textAnchor: 'middle', fontSize: graphOptions["font-size"] }} />}
                                        />}

                                    {(meteorologicalGraphLines.length === 0) ? null :
                                        <YAxis yAxisId="right" orientation="right" label={<Label
                                            value="Meteorological"
                                            position="insideRight"
                                            angle={90}
                                            style={{ textAnchor: 'middle', fontSize: graphOptions["font-size"] }} />}
                                        />}

                                    <CartesianGrid strokeDasharray="3 3" />
                                    <Tooltip />

                                    {graphOptions["legend"] ?
                                        <Legend dy={10}
                                            wrapperStyle={{ position: 'relative', marginTop: '16px' }}
                                        />
                                        : null}

                                    {(irridianceGraphLines.length === 0) ? null :
                                        irridianceGraphLines.map((line_name, index) => (
                                            <Line
                                                yAxisId="left"
                                                type="monotone"
                                                key={`left-${line_name}`}
                                                dataKey={line_name}
                                                stroke={graphColors[graphLines[line_name]]}
                                                strokeWidth={graphOptions["line-thickness"]}
                                                fillOpacity={1}
                                                // fill="url(#colorUv)"
                                                dot={graphOptions["dot"] ? { strokeWidth: 1, r: 1 } : false}
                                            />
                                        ))}

                                    {(meteorologicalGraphLines.length === 0) ? null :
                                        meteorologicalGraphLines.map((line_name, index) => (
                                            <Line
                                                yAxisId="right"
                                                type="linear"
                                                key={`right-${line_name}`}
                                                dataKey={line_name}
                                                stroke={graphColors[graphLines[line_name]]}
                                                strokeWidth={graphOptions["line-thickness"]}
                                                fillOpacity={1}
                                                // fill="url(#colorUv)"
                                                dot={graphOptions["dot"] ? { strokeWidth: 1, r: 1 } : false}
                                            />
                                        ))}
                                </LineChart>
                            </>
                        </div>
                    </div>
                </Resizable>
            </div>

            <Form>
                <Form.Check>
                    <Form.Check inline label="csv" name="group1" type='radio' id={`inline-radio-0`} checked={downloadSelection === 0} value={0} onClick={() => setDownloadSelection(0)} />
                    <Form.Check inline label="zip compressed" name="group1" type='radio' id={`inline-radio-1`} checked={downloadSelection === 1} value={1} onClick={() => setDownloadSelection(1)} />
                    <Form.Check inline label="json" name="group1" type='radio' id={`inline-radio-5`} checked={downloadSelection === 5} value={5} onClick={() => setDownloadSelection(5)} />
                    <Form.Check inline label="png" name="group1" type='radio' id={`inline-radio-2`} checked={downloadSelection === 2} value={2} onClick={() => setDownloadSelection(2)} />
                    <Form.Check inline label="jpeg" name="group1" type='radio' id={`inline-radio-3`} checked={downloadSelection === 3} value={3} onClick={() => setDownloadSelection(3)} />
                    <Form.Check inline label="svg" name="group1" type='radio' id={`inline-radio-4`} checked={downloadSelection === 4} value={4} onClick={() => setDownloadSelection(4)} />

                </Form.Check>

                <Button variant="primary" style={{ margin: "20px 0px 10px 50px" }} onClick={handleChartSubmit}>
                    Download Data
                </Button>
            </Form>

        </div>
    )
}

export default Chart