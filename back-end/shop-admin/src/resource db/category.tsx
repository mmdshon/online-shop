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
    ReferenceField,
    ShowButton
} from 'react-admin';
import { Stack } from '@mui/material';

const CategoryFilters = [
    <SearchInput source="name" alwaysOn />,
    <TextInput label="email" source="email" defaultValue="irmrbug@gmail.com" />,
];
const ListToolbar = () => (
    <Stack direction="row" justifyContent="space-between">
        <FilterForm filters={CategoryFilters} />
        <div>
            <FilterButton filters={CategoryFilters} />
            <CreateButton />
        </div>
    </Stack>
)
export const CategoryList = () => (
    <List>
        <ListToolbar />
        <Datagrid rowClick="edit">
            <TextField source="id" />
            <TextField source="name" />
            <TextField source="description" />
            <ReferenceField source="parent_category_id" reference="Categories" link="show" />
            <DateField source="created_at" />
            <ShowButton label='show'/>
        </Datagrid>
    </List>
);