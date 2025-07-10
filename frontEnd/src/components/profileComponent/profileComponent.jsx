import React, { useEffect, useState } from 'react';
import {
    Box,
    Button,
    Flex,
    FormControl,
    FormLabel,
    Heading,
    Input,
    VStack,
} from "@chakra-ui/react";
import { getUserDatasAPI } from '../../service/userService.js';

export default function ProfileComponent() {
  const [formData, setFormData] = useState(null);


  useEffect(() => {
    const getUserDatas = async () => {
      try {
        const datas = await getUserDatasAPI();
        console.log(datas)
        setFormData(datas);
      } catch (err) {
        console.log(err);
      } finally {
    
      }
    };

    getUserDatas();
  }, []);


  return (
    <Flex
      color="white"
      align="center"
      justify="center"
    >
      <Box
        bg="gray.800"
        p={8}
        borderRadius="xl"
        boxShadow="lg"
        w="lg"
      >

        <VStack spacing={4}>
          <FormControl>
            <FormLabel>Nome</FormLabel>
            <Input
              placeholder="Nome"
              name="name"
              borderColor="whiteAlpha.500"
              _placeholder={{ color: "gray.400" }}
              value={formData?.userName || "carregando..."}
              //onChange={handleChange}
              _hover={{ borderColor: "white" }}
              _focus={{ borderColor: "white" }}
              rounded="full"
            />
          </FormControl>

          <FormControl>
            <FormLabel>Email</FormLabel>
            <Input
              placeholder="Email"
              name="email"
              type="email"
              borderColor="whiteAlpha.500"
              value={formData?.userEmail || "carregando..."}
              //onChange={handleChange}
              _placeholder={{ color: "gray.400" }}
              _hover={{ borderColor: "white" }}
              _focus={{ borderColor: "white" }}
              rounded="full"
            />
          </FormControl>


          <Button
            bg="#346E62"
            _hover={{ bg: "#419181" }}
            color="white"
            rounded="full"
            //onClick={handleSubmit}
            w="full"
            mt={4}
            //isLoading={isFetching}
            loadingText="Enviando..."
          >
            Enviar
          </Button>
        </VStack>
      </Box>
    </Flex>
  );
}
