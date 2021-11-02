import * as typeorm from 'typeorm';

@typeorm.Entity()
@typeorm.Index(['owner', 'updatedAt'])
export class Ticket {
  @typeorm.PrimaryColumn({ type: 'uuid' })
  id!: number;

  @typeorm.Column()
  owner!: string;

  @typeorm.Column()
  description!: string;

  @typeorm.CreateDateColumn({ type: 'timestamp with time zone', name: 'created_at' })
  createdAt!: Date;

  @typeorm.UpdateDateColumn({ type: 'timestamp with time zone' })
  updatedAt!: Date;

  @typeorm.Column({ type: 'timestamp with time zone', nullable: true })
  resolvedAt?: Date;
}

// npx typeorm migration:generate --name tickets
// npx typeorm migration:run
// npx typeorm migration:generate --name rename
