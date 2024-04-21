import {
    CreateButton,
    Datagrid,
    FilterButton,
    FilterForm,
    ListBase,
    List,
    Pagination,
    TextField,
    TextInput,
    SearchInput,
    EmailField,
    DateField,
    ShowButton,
} from 'react-admin';
import { Stack } from '@mui/material';

const CustomerFilters = [
    <SearchInput source="Name" resettable alwaysOn />,
    <TextInput label="email" source="Email" />
];
const ListToolbar = () => (
    <Stack direction="row" justifyContent="space-between">
        <FilterForm filters={CustomerFilters} />
        <div>
            <FilterButton filters={CustomerFilters} />
            <CreateButton />
        </div>
    </Stack>
)
export const UsersList = () => (
    <List>
        <ListToolbar />
        <Datagrid rowClick="edit">
            <TextField disabled source="id" />
            <TextField source="Name"/>
            <TextField source="Password"/>
            <EmailField source="Email"/>
            <TextField source="Phone"/>
            <DateField disabled source="registration_date" />
            <TextField source="Role" />
            <TextField source="address" />
            <ShowButton label='show'/>
        </Datagrid>
    </List>
);