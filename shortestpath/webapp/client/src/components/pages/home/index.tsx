import * as React from "react";
import { Button, Col, Container, Form, Row } from "reactstrap";
import "./home_style.scss";
import { ArticleTitle, KnownError, getStoredToken } from "@home/request";
import SearchInput from "./SearchInput";
import { FindShortestPath } from "@home/request";
import PathDisplay from "./PathDisplay";
import WikiSPLogo from "../WikiSPLogo";
import ErrorDisplay, { ErrorProps, ErrorType } from "./ErrorDisplay";
import CaptchaVerification from "./CaptchaVerification";

function HomePage() {
    const [input1Val, setInput1Val] = React.useState("");
    const [input2Val, setInput2Val] = React.useState("");
    const [searchInProgress, setSearchInProgress] = React.useState(false);

    const findPathButtonDisabled = input1Val === "" || input2Val === "" || searchInProgress === true;

    const [askCaptcha, setAskCaptcha] = React.useState(false);

    const defaultPathVal: ArticleTitle[] = [] // To avoid typescript casting to any[]
    const [path, setPath] = React.useState(defaultPathVal);
    const defaultValError: ErrorProps = null;
    const [errorDisplayProps, setErrorDisplayProps] = React.useState(defaultValError);

    function captchaCallBack(success: boolean) {
        if (success === true) {
            handleFormSubmit(null);
        } else {
            setErrorDisplayProps({type: ErrorType.INTERNAL_ERROR});
        }

        setAskCaptcha(false);
    }

    function closedCaptchaCallback() {
        setAskCaptcha(false);
    }

    async function handleFormSubmit(event: React.FormEvent) {
        if (event != null) {
            event.preventDefault();
        }

        if (getStoredToken() === null && BUILDCONFIG.captchaEnabled) {
            setAskCaptcha(true);
            return;
        }

        setErrorDisplayProps(null);
        setPath([]);
        setSearchInProgress(true);

        try {
            const pathResult = await FindShortestPath(input1Val, input2Val);
            
            if (pathResult.length === 0) {
                setErrorDisplayProps({type: ErrorType.NO_PATH});
            } else {
                setPath(pathResult);
            }
        } catch(err) {
            if (err.type === KnownError.INVALID_PARAMETER) {
                setErrorDisplayProps({type: ErrorType.INVALID_ARTICLE, additionalInfo: err.additionalInfo});
            } else if (err.type === KnownError.UNAUTHORIZED) {
                setAskCaptcha(true);
            } else {
                setErrorDisplayProps({type: ErrorType.INTERNAL_ERROR});
            }
        } finally {
            setSearchInProgress(false);
        }
    }

    return <>
        { askCaptcha ? <CaptchaVerification isOpen={true} verifCallback={captchaCallBack} closedCallback={closedCaptchaCallback} /> : null }
        <Container fluid className="typical-page-layout">
        <Row className="space-after-title">
            <WikiSPLogo/>
            <Row>
                <Col>
                <p className="wikisp-desc d-none d-md-block">
                <a target="_blank" href="https://en.wikipedia.org/wiki/Wikipedia:Six_degrees_of_Wikipedia">Six Degrees of Wikipedia</a> is a captivating concept inspired by the theory of six degrees of separation, 
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
        {errorDisplayProps === null ? null : <ErrorDisplay type={errorDisplayProps.type} additionalInfo={errorDisplayProps.additionalInfo}/>}
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
        <a target="_blank" href="https://github.com/haskaalo/wikisp">GitHub repository</a>
        </div>
    </div>
    </>;
}

export default HomePage;
