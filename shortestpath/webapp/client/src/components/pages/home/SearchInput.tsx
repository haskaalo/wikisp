import * as React from "react";
import { SearchArticleTitle, GetRandomArticleTitles } from "@home/request";
import { Input, ListGroup, ListGroupItem } from "reactstrap";

interface IProps {
    onInputChange: (value: string) => void;
    disabled: boolean
}

function SearchInput(props: IProps) {
    const defaultVal: string[] = [] // So typescript doesnt cast to any[] xd
    const [inputResults, setInputResults] = React.useState(defaultVal);
    const [inputPreviousResults, setInputPreviousResults] = React.useState(defaultVal);
    const [inputPlaceholderVal, setInputPlaceholderVal] = React.useState("");
    const [inputVal, setInputVal] = React.useState("");
    const inputValRef = React.useRef(inputVal); // Necessary for access inside timeout
    inputValRef.current = inputVal;

    const searchTimeoutInProgress = React.useRef(false);
    const searchTimeout = React.useRef(setTimeout(() => {}, 0));

    async function handleInputChange(event: React.ChangeEvent<HTMLInputElement>) {
        async function doSearchResult() {
            const searchResult = await SearchArticleTitle(inputValRef.current);
            setInputResults(searchResult);
            searchTimeoutInProgress.current = false;
        }

        setInputVal(event.currentTarget.value);
        props.onInputChange(event.currentTarget.value);

        if (event.currentTarget.value == "") {
            setInputResults([]);
            return;
        }

        if (searchTimeoutInProgress) {
            clearTimeout(searchTimeout.current);
        }
    
        searchTimeoutInProgress.current = true;
        searchTimeout.current = setTimeout(() => {
            doSearchResult();
        }, 300);
    }
    function hideSearch() {
        setInputResults([]);
        setInputPreviousResults(inputResults);
    }

    function inputBlurEvent(e: React.FocusEvent) {
        // Search item has been pressed so we need to skip call to hideSearch
        // and allow onClick to be called
        if (e.relatedTarget != null && e.relatedTarget.classList.contains("search-item")) {
            return;
        }

        hideSearch();
    }

    function inputFocusEvent() {
        setInputResults(inputPreviousResults);
    }

    function handleSearchItemClick(query: string) {
        setInputVal(query);
        props.onInputChange(query);
        hideSearch();
    }

    function handleKeyDown(e: React.KeyboardEvent, query: string) {
        if (e.key === "Enter") {
            handleSearchItemClick(query);
        }
    }

    React.useEffect(() => {
        const interval = setInterval(async () => {
            const articleTitles = await GetRandomArticleTitles();
            let newVal = articleTitles[Math.floor(Math.random() * articleTitles.length)];

            for (let i = 0; i < newVal.length; i++) {
                setInputPlaceholderVal(newVal.slice(0, i+1));
                await new Promise(r => setTimeout(r, Math.ceil(1000 / newVal.length)));
            }
            await new Promise(r => setTimeout(r, 1000));

            // If you ever wonder why i dont use inputPlaceholderVal, its cus its empty for some reason
            const initialLength = newVal.length;
            while (newVal.length > 0) {
                newVal = newVal.slice(0, newVal.length - 1)
                setInputPlaceholderVal(newVal.slice(0, newVal.length - 1));
                
                await new Promise(r => setTimeout(r, 1000 / initialLength));
            }
        }, 3500);

        return () => clearInterval(interval);
    }, []);

    if (props.disabled && inputResults.length > 0) {
        hideSearch();
    }
    
    return <>
        <Input bsSize="lg" onChange={handleInputChange} onBlur={inputBlurEvent} onFocus={inputFocusEvent}
        value={inputVal}
        placeholder={inputPlaceholderVal} 
        className="shadow"
        disabled={props.disabled}
        />
        <ListGroup hidden={props.disabled} style={{position: "absolute"}}>
            {inputResults.map(s => <ListGroupItem key={s} onClick={() => handleSearchItemClick(s)} 
            className="search-item" tabIndex={0} onKeyDown={(e) => handleKeyDown(e, s)}>
                {s}</ListGroupItem>)}
        </ListGroup>
    </>
}

export default SearchInput;