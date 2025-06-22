import React from 'react';
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  IconButton,
} from '@chakra-ui/react';
import { FiMoreVertical, FiEye, FiEdit2, FiTrash2 } from 'react-icons/fi';
import styles from './videoList.module.css'

export default function VideoList({ videos, onDelete, onEdit, onView, selected, onSelect }) {
  const getStatusStyles = (status) => {
    switch (status.toUpperCase()) {
      case 'PROCESSING':
      case 'PROCESSANDO':
        return {
          bg: 'yellow.300',
          color: '#222',
        };
      case 'READY':
      case 'DISPONIVEL':
        return {
          bg: 'green.200',
          color: 'green.800',
        };
      case 'FAIL':
      case 'FAILED':
      case 'FALHOU':
        return {
          bg: 'red.300',
          color: 'red.800',
        };
      default:
        return {
          bg: 'gray.200',
          color: 'gray.800',
        };
    }
  };

  return (
    <div className={styles.container}>
    <Box overflowX="auto" borderWidth="0px" borderRadius="md" bg="#222" color="white" p={4}>
     <Table variant="simple" size="sm" sx={{ 'td, th': {borderBottomColor: '#222',},}}>
        <Thead>
          <Tr>
            <Th color="gray.400">Data</Th>
            <Th color="gray.400">Título</Th>
            <Th color="gray.400" >Status</Th>
            <Th color="gray.400" textAlign="center">Ações</Th>
          </Tr>
        </Thead>
        <Tbody>
          {videos.map((video) => {
            const statusStyles = getStatusStyles(video.status);

            return (
              <Tr key={video.videoId} _hover={{ bg: 'gray.800' }}>
                <Td>{video.date}</Td>
                <Td>{video.title || 'Sem título'}</Td>
                <Td>
                  <Badge
                    px={3}
                    py={1}
                    borderRadius="full"
                    bg={statusStyles.bg}
                    color={statusStyles.color}
                    fontWeight="bold"
                  >
                    {video.status.toUpperCase() === 'PROCESSING'
                      ? 'Processando'
                      : video.status.toUpperCase() === 'READY'
                      ? 'Disponível'
                      : video.status.toUpperCase() === 'FAIL'
                      ? 'Falhou'
                      : video.status}
                  </Badge>
                </Td>
                <Td textAlign="center">
                  <Menu>
                    <MenuButton
                      as={IconButton}
                      aria-label="Opções"
                      icon={<FiMoreVertical />}
                      size="sm"
                      variant="ghost"
                      color="gray.300"
                      _hover={{ bg: 'gray.700' }}
                    />
                    <MenuList bg="#222" borderColor="black">
                      <MenuItem
                        icon={<FiEye color="white" />}
                        bg="#222"
                        color="white"
                        _hover={{ bg: 'gray.700' }}
                        onClick={() => onView(video.videoId)}
                      >
                        Visualizar
                      </MenuItem>
                      <MenuItem
                        icon={<FiEdit2 color="white" />}
                        bg="#222"
                        color="blue.300"
                        _hover={{ bg: 'gray.700' }}
                        onClick={() => onEdit(video.videoId)}
                      >
                        Editar
                      </MenuItem>
                      <MenuItem
                        icon={<FiTrash2 color="red" />}
                        bg="#222"
                        color="red.300"
                        _hover={{ bg: 'gray.700' }}
                        onClick={() => onDelete(video.videoId)}
                      >
                        Deletar
                      </MenuItem>
                    </MenuList>
                  </Menu>
                </Td>
              </Tr>
            );
          })}
        </Tbody>
      </Table>
    </Box>
    </div>
  );
}
