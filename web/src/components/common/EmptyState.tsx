import React from 'react';
import {CircularProgress} from '@mui/material';

interface EmptyStateProps {
  emptyText: string;
  children: React.ReactNode;
  isEmpty: boolean;
  isLoading: boolean;
}

export default function EmptyState(props: EmptyStateProps): React.ReactNode {
  if (props.isEmpty || props.isLoading) {
    return (
      <div className='fill-height' style={{alignItems: 'center', justifyContent: 'center'}}>
        {props.isLoading ? <CircularProgress /> : props.emptyText}
      </div>
    );
  }

  return props.children;
}
