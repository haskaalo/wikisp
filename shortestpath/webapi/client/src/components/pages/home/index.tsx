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
            <Row>
                <Col>
                <p className="wikisp-desc d-none d-md-block">
                Six Degrees of Wikipedia is a captivating concept inspired by the theory of six degrees of separation, 
                commonly used in social networks, demonstrating that any two Wikipedia articles can be connected within six clicks
                or fewer. This project specifically focuses on uncovering the shortest path between articles on the English version of Wikipedia, 
                exploring the vast web of interconnected knowledge present on the platform.
                </p>
                <p className="wikisp-desc d-md-none">
                Six Degrees of Wikipedia is a captivating concept demonstrating that any two Wikipedia articles can be connected within six clicks
                or fewer. This project focuses on uncovering the shortest path between articles on the English version of Wikipedia
                </p>
                </Col>
            </Row>
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
    <div className="footer">
        <div className="footer-text">
        Made with ❤️ by Joey
        <br/>
        <a href="https://github.com/haskaalo/wikisp">GitHub repository</a>
        </div>
    </div>
    </>;
}

export default HomePage;
