import * as React from "react";
import { Button, Col, Container, Form, Row } from "reactstrap";
import "./home_style.scss";
import { ArticleTitle } from "@home/request";
import SearchInput from "./SearchInput";
import { FindShortestPath } from "@home/request";
import PathDisplay from "./PathDisplay";

function HomePage() {
    const [input1Val, setInput1Val] = React.useState("");
    const [input2Val, setInput2Val] = React.useState("");
    const findPathButtonDisabled = input1Val === "" || input2Val === "";

    const defaultPathVal: ArticleTitle[] = [] // To avoid typescript casting to any[]
    const [path, setPath] = React.useState(defaultPathVal);

    async function handleFormSubmit(event: React.FormEvent) {
        event.preventDefault();

        // TODO: catch error lol
        const pathResult = await FindShortestPath(input1Val, input2Val);
        setPath(pathResult);
    }

    return <>
        <Container fluid className="typical-page-layout">
        <Row className="space-after-title">
            <h1 style={{textAlign: "center"}}>WikiSP</h1>
        </Row>
        <Form onSubmit={handleFormSubmit}>
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
                    <Button type="submit"  style={{width: "100%"}} disabled={findPathButtonDisabled}>Find path!</Button>
                </Col>
                <Col/>
            </Row>
        </Form>
    </Container>
    <Container fluid className="typical-page-layout">
        <Row>
            {path.length === 0 ? null : <PathDisplay path={path}/>}
        </Row>
    </Container>
    </>;
}

export default HomePage;
