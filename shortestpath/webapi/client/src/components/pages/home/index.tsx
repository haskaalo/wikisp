import * as React from "react";
import { Button, Col, Container, Form, Row } from "reactstrap";
import "./home_style.scss";
import { ArticleTitle, KnownError } from "@home/request";
import SearchInput from "./SearchInput";
import { FindShortestPath } from "@home/request";
import PathDisplay from "./PathDisplay";
import WikiSPLogo from "../WikiSPLogo";

function HomePage() {
    const [input1Val, setInput1Val] = React.useState("");
    const [input2Val, setInput2Val] = React.useState("");
    const [searchInProgress, setSearchInProgress] = React.useState(false);

    const findPathButtonDisabled = input1Val === "" || input2Val === "" || searchInProgress === true;

    const defaultPathVal: ArticleTitle[] = [] // To avoid typescript casting to any[]
    const [path, setPath] = React.useState(defaultPathVal);

    async function handleFormSubmit(event: React.FormEvent) {
        event.preventDefault();
        setPath([]);
        setSearchInProgress(true);

        try {
            const pathResult = await FindShortestPath(input1Val, input2Val);
            if (pathResult.length === 0) {
                alert("No path possible!");
            } else {
                setPath(pathResult);
            }
        } catch(err) {
            if (err.message === KnownError.INVALID_PARAMETER) {
                // TODO: Change this
                alert("An article doesn't exist");
            } else {
                alert("Internal error");
            }
        }

        setSearchInProgress(false);
    }

    return <>
        <Container fluid className="typical-page-layout">
        <Row className="space-after-title">
            <WikiSPLogo/>
        </Row>
        <Form onSubmit={handleFormSubmit}>
            <Row className="space-after-inputs">
                <Col md="6" className="between-input-small-space">
                    <SearchInput onInputChange={setInput1Val} disabled={searchInProgress} />
                </Col>
                <Col md="6">
                    <SearchInput onInputChange={setInput2Val} disabled={searchInProgress} />
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
    {path.length === 0 ? null : <PathDisplay path={path}/>}
    </>;
}

export default HomePage;
