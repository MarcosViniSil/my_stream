import {
  Input,
  InputGroup,
  InputLeftElement,
  Button,
  Stack,
  useBreakpointValue,
} from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";
import { useState } from "react";

function SearchBar({ onSearch }) {
  const [searchTerm, setSearchTerm] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSearch) onSearch(searchTerm);
  };

  const stackDirection = useBreakpointValue({ base: "row", md: "row" });

  return (
    <form onSubmit={handleSubmit}>
      <Stack direction={stackDirection} spacing={2}>
        <InputGroup width={{ md: "300px" }}>
          <InputLeftElement pointerEvents="none">
            <SearchIcon />
          </InputLeftElement>
          <Input
            type="text"
            placeholder="Busque um vídeo"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            bg="white"
            color="black"
            border="none"
            _focus={{ boxShadow: "none", border: "none" }}
          />
        </InputGroup>

        <Button
          type="submit"
          className="buttonSendSearch"
          color="white"
          backgroundColor="#419181"
          _hover={{
            backgroundColor: "#2f6f60",
          }}
          _active={{
            backgroundColor: "#265a4f",
          }}
          _focus={{
            boxShadow: "0 0 0 2px #265a4f",
          }}
        >
          <SearchIcon />
        </Button>
      </Stack>
    </form>
  );
}

export default SearchBar;
