import * as React from "react";
import { Button, Col, Container, Row } from "reactstrap";
import "./home_style.scss";
import SearchInput from "./SearchInput";

function HomePage() {
    const [input1Val, setInput1Val] = React.useState("");
    const [input2Val, setInput2Val] = React.useState("");

    return <Container fluid className="typical-page-layout">
        <Row className="space-after-title">
            <h1 style={{textAlign: "center"}}>WikiSP</h1>
        </Row>
        <Row className="space-after-inputs">
            <Col md="6" className="between-input-small-space">
                <SearchInput onInputChange={setInput1Val}/>
            </Col>
            <Col md="6">
                <SearchInput onInputChange={setInput2Val} />
            </Col>
        </Row>
        <Row>
            <Col/>
            <Col md="4">
                <Button style={{width: "100%"}}>Find path!</Button>
            </Col>
            <Col/>
        </Row>
    </Container>;
}

export default HomePage;
